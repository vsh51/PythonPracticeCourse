import requests
import telebot
import PngFormatter.discipline_statistics_charts as dsc
import SQLConnection
import os
from datetime import datetime, timedelta
import requests
import signal
import sys

from dotenv import load_dotenv
load_dotenv()

database=SQLConnection.SQLConnectionWrapper(
     os.environ.get('SERVER'),
     os.environ.get('MYSQL_USER'),
     os.environ.get('MYSQL_PASSWORD'),
     os.environ.get('MYSQL_DATABASE')
).__enter__()


TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(str(TOKEN))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    reply_message="Hello! I am a grade bot. Enter /help to learn more."
    bot.reply_to(message, reply_message)
    
    if not database.user_exists(message.from_user.id):
        database.create_user(message.from_user.username, message.from_user.id)
        bot.send_message(message.chat.id, "You have successfully created an account!")
    else:
        bot.send_message(message.chat.id, "You already have an account, welcome back!")


@bot.message_handler(commands=['help'])
def send_help(message):
    reply_message = (
        "First, create a list of your disciplines, only then you will be able to add grades to the corresponding discipline\n\n"
        "Available commands:\n\n"
        "/start - Start working with the bot\n"
        "/help - Show this message\n"
        "/add_discipline - Add a discipline\n"
        "/remove_discipline - Remove a discipline\n"
        "/all_disciplines - List all disciplines\n"
        "/submit_grade - Add a grade for the selected discipline\n"
        "/remove_grade - Remove the last grade of the discipline\n"
        "/show_grades_list - Show the list of grades for the selected discipline\n"
        "/discipline_statistic - Show the pie chart of the selected discipline\n"
        "/last_n_days_chart - Show the chart of the discipline progress over the last n days\n"
        "/delete_account - Delete your account\n"
    )
    bot.reply_to(message, reply_message)


@bot.message_handler(commands=['submit_grade'])
def submit_grade_handler(message):
    bot.reply_to(message, "Please enter the discipline name, grade type (p/l), and the grade. Example: 'Math p 85'")
    bot.register_next_step_handler(message, process_grade_input)

def process_grade_input(message):
    gtype = {'p': 'practice', 'l': 'lecture'}

    try:
        input_data = message.text.split()

        if len(input_data) != 3:
            raise Exception("Invalid format. Please provide discipline_name, grade_type (p/l), and grade.")

        discipline_name, grade_type, gr = input_data
        grade = int(gr)

        if not database.discipline_exists(message.from_user.id, discipline_name):
            raise Exception("There is no such discipline in your list. Add discipline /add_discipline")
        if grade_type not in ['p', 'l']:
            raise Exception("Invalid grade type. It must be either 'p' (practice) or 'l' (lecture).")
        if grade < 0 or grade > 100:
            raise Exception("Your grade must be between 0 and 100.")

        pints = database.get_points_by_discipline(message.from_user.id, discipline_name)

        if pints["practice_total_points"] < sum([e['value'] for e in pints['points']['practice']]) + grade and grade_type == 'p':
            raise Exception("You have reached the maximum number of points for practice")
        if pints["lecture_total_points"] < sum([e['value'] for e in pints['points']['lecture']]) + grade and grade_type == 'l':
            raise Exception("You have reached the maximum number of points for lecture")

        bot.reply_to(message, f"Grade {grade} for {discipline_name} ({grade_type}) submitted successfully!")
        database.create_point(message.from_user.id,
                              discipline_name,
                              SQLConnection.PointType.from_string(gtype[grade_type]),
                              grade,
                              datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))

    except ValueError:
        bot.reply_to(message, "You entered an invalid grade. Please enter a numeric value between 0 and 100.")
    except Exception as e:
        bot.reply_to(message, str(e))


@bot.message_handler(commands=['remove_grade'])
def remove_grade_handler(message):
    bot.reply_to(message, "Please enter the discipline_name (use _ instead spaces)")
    bot.register_next_step_handler(message, grade_to_remove_input)

def grade_to_remove_input(message):
    try:
        command_list = message.text.split()
        if len(command_list) != 1:
            raise Exception("Invalid format. It must be like: discipline_name")

        discipline_name = command_list[0]

        if not database.discipline_exists(message.from_user.id, discipline_name):
            raise Exception("There is no such discipline in your list. Add discipline /add_discipline")
        if not database.points_exist(message.from_user.id, discipline_name):
            raise Exception("There are no grades for this discipline")
        else:
            removed_gr = database.remove_last_point(message.from_user.id, discipline_name)
            bot.reply_to(message, f"Grade {removed_gr} removed successfully!")
            return

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")


@bot.message_handler(commands=['show_grades_list'])
def show_grade_list_handler(message):
    bot.reply_to(message, "Please enter the discipline_name (use _ instead spaces)")
    bot.register_next_step_handler(message, discipline_to_show_list_input)

def discipline_to_show_list_input(message):
    try:
        command_list = message.text.split()
        if len(command_list) != 1:
            raise Exception("Invalid format. It must be like: discipline_name")

        discipline_name = command_list[0]

        if not database.discipline_exists(message.from_user.id, discipline_name):
            raise Exception("There is no such discipline in your list. Add discipline /add_discipline")
        if not database.points_exist(message.from_user.id, discipline_name):
            raise Exception("There are no grades for this discipline")
        else:
            grades_list = database.get_points_by_discipline(message.from_user.id, discipline_name)
            
            header = f"Grades for {discipline_name}:"
            if grades_list['points']['lecture']:
                lectures = f"Lecture: {', '.join(map(str, [e['value'] for e in grades_list['points']['lecture']]))}"
            else:
                lectures = "Lecture: 0"

            if grades_list['points']['practice']:
                practice = f"Practice: {', '.join(map(str, [e['value'] for e in grades_list['points']['practice']]))}"
            else:
                practice = "Practice: 0"

            bot.reply_to(message, f"{header}\n{lectures}\n{practice}")

    except Exception as e:
        bot.reply_to(message, str(e))


@bot.message_handler(commands=['add_discipline'])
def add_discipline(message):
    bot.reply_to(message, "Please enter the discipline_name (use _ instead spaces)")
    bot.register_next_step_handler(message, discipline_to_add_input)

def discipline_to_add_input(message):
    try:
        command_list = message.text.split()
        if len(command_list) != 1:
            raise Exception("Invalid format. It must be like: discipline_name")

        if database.discipline_exists(message.from_user.id, command_list[0]):
            raise Exception("The discipline already exists")
        else:
            database.create_discipline(message.from_user.id, command_list[0], 50, 50)

        bot.reply_to(message, f"Discipline '{command_list[0]}' submitted successfully!")

    except Exception as e:
        bot.reply_to(message, f"Error: {e}")


@bot.message_handler(commands=['remove_discipline'])
def remove_discipline(message):
    bot.reply_to(message, "Please enter the discipline_name (use _ instead spaces)")
    bot.register_next_step_handler(message, discipline_to_remove)

def discipline_to_remove(message):
    try:
        command_list = message.text.split()
        if len(command_list) != 1:
            raise Exception("Invalid format. It must be like: discipline_name")

        dis_name = command_list[0]
        if not database.discipline_exists(message.from_user.id, dis_name):
            raise Exception("The discipline does not exist in your list")
        else:
            database.delete_discipline(message.from_user.id, dis_name)
            bot.reply_to(message, f"Discipline {dis_name} was removed successfully")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")


@bot.message_handler(commands=['all_disciplines'])
def show_disciplines_list(message):
    command_list = message.text.split()
    if len(command_list) != 1:
        raise Exception("Invalid format. It must be like: /all_disciplines")

    if database.get_disciplines_list(message.from_user.id) == []:
        bot.reply_to(message, "Your discipline list is empty")
    else:
        bot.reply_to(message, f"Your disciplines: {', '.join(database.get_disciplines_list(message.from_user.id))}")


@bot.message_handler(commands=['discipline_statistic'])
def show_discipline_chart(message):
    bot.reply_to(message, "Please enter the names of the discipline (use _ instead spaces)")
    bot.register_next_step_handler(message, discipline_to_show_chart)

def discipline_to_show_chart(message):
    try:
        command_list = message.text.split()
        if len(command_list) != 1:
            raise Exception("Invalid format. It must be like: discipline")

        dis_name = command_list[0]
        if not database.discipline_exists(message.from_user.id, dis_name):
            raise Exception("The discipline is not listed")

        if not database.points_exist(message.from_user.id, dis_name):
            bot.reply_to(message, "You have no data to make chart")
        else:
            points = database.get_points_by_discipline(message.from_user.id, dis_name)
            discip1 = dsc.Discipline(points)
            ch = dsc.ChartMaker()
            filename = ch.make_pie_chart(discip1)
            with open(filename, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
            os.remove(filename)

    except Exception as e:
        bot.reply_to(message, str(e))


@bot.message_handler(commands=['last_n_days_chart'])
def n_days_chart(message):
    bot.reply_to(message, "Please enter the number of last days and the discipline. Example: '7 Math'")
    bot.register_next_step_handler(message, process_compare_discipline_input)

def process_compare_discipline_input(message):
    try:
        input_data = message.text.split()

        if len(input_data) != 2:
            raise Exception("Invalid format. Please provide number_of_days and one discipline.")

        number_of_days = int(input_data[0])
        discipline_name = input_data[1]

        if not database.discipline_exists(message.from_user.id, discipline_name):
            raise Exception(
                f"The discipline {discipline_name} does not exist in your list. Add discipline using /add_discipline")

        end_date = datetime.now()
        start_date = end_date - timedelta(days=number_of_days)

        grades = database.get_points_for_discipline_in_range(message.from_user.id, discipline_name, start_date,
                                                             end_date)
        if not grades:
            bot.reply_to(message, "No grades found for the selected discipline in the given date range.")
            return

        discipline = dsc.Discipline(grades)
        chart_maker = dsc.ChartMaker()
        filename = chart_maker.make_n_days_chart(discipline, start_date, end_date)
    
        bot.reply_to(message,
                     f"Here is the progress of your discipline '{discipline_name}' over the last {number_of_days} days.")

        with open(filename, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        os.remove(filename)

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")
        bot.register_next_step_handler(message, process_compare_discipline_input)


@bot.message_handler(commands=['delete_account'])
def delete_account(message):
    bot.reply_to(message, "Are you sure you want to delete your account? (yes/no)")
    bot.register_next_step_handler(message, delete_account_confirm)

def delete_account_confirm(message):
    if message.text.lower() == 'yes':
        if not database.user_exists(message.from_user.id):
            bot.reply_to(message, "You do not have an account.")
            return
        database.delete_user(message.from_user.id)
        bot.reply_to(message, "Your account has been successfully deleted.")
    elif message.text.lower() == 'no':
        bot.reply_to(message, "Your account has not been deleted.")
    else:
        bot.reply_to(message, "Invalid input. Please enter 'yes' or 'no'.")


@bot.message_handler(func=lambda message: True)
def handle_unknown_text(message):
    try:
        bot.reply_to(message, "Sorry, I don't understand this command or text. Take a kitty instead. Try /help")

        response = requests.get("https://api.thecatapi.com/v1/images/search")
        if response.status_code == 200:
            cat_data = response.json()
            cat_image_url = cat_data[0]["url"]

            bot.send_photo(message.chat.id, cat_image_url)
        else:
            bot.reply_to(message, "Sorry, I couldn't fetch a cat image right now. Try again later.")

    except Exception as e:
        bot.reply_to(message, f"An error occurred while fetching the cat image: {str(e)}")


if __name__ == "__main__":
    def signal_handler(sig, frame):
        database.__exit__(None, None, None)
        print("Exiting...")
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    bot.infinity_polling()
    signal.pause()
