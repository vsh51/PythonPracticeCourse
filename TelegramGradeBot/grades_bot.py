import telebot
from PngFormatter import discipline_statistics_charts as dsc
import SQLConnection
import os

# database=SQLConnection.SQLConnectionWrapper(
#             os.environ.get('SERVER'),
#             os.environ.get('MYSQL_USER'),
#             os.environ.get('MYSQL_PASSWORD'),
#             os.environ.get('MYSQL_DATABASE'))

TOKEN="7227677197:AAEAJPpPqEdFICLGraX5kmnZ-77KuMYJZe4"
"""TOKEN = "7740781215:AAHKs_1YFhVueNbPbx93XreIH5WrpQANtrQ"""""
bot = telebot.TeleBot(TOKEN)

discipline_names=[]
disciplines={}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    reply_message="Hello! I am a grade bot. Enter /help to learn more."
    bot.reply_to(message, reply_message)

    # bot.reply_to(message, message.from_user.username)
    # bot.reply_to(message, message.from_user.id)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    reply_message = (
        "First, create a list of your disciplines, only then you will be able to add grades to the corresponding discipline\n\n\n"
        "Available commands:\n\n"
        "/start - Start working with the bot\n"
        "/help - Show this message\n"
        "/add_discipline - Add a discipline\n"
        "/remove_discipline - Remove a discipline\n"
        "/all_disciplines - List all disciplines\n"
        "/submit_grade - Add a grade for the selected discipline\n"
        "/remove_grade - Remove the last grade of the discipline\n"
        "/show_grades_list - Show the list of grades for the selected discipline\n"
        "/discipline_chart - Display the grade chart for the discipline\n"
    )
    bot.reply_to(message, reply_message)


@bot.message_handler(commands=['submit_grade'])
def submit_grade_handler(message):
    bot.reply_to(message, "Please enter the discipline name, grade type (p/l), and the grade. Example: 'Math p 85'")

    bot.register_next_step_handler(message, process_grade_input)

def process_grade_input(message):
    try:
        input_data = message.text.split()

        if len(input_data) != 3:
            raise Exception("Invalid format. Please provide discipline_name, grade_type (p/l), and grade.")

        discipline_name, grade_type, gr = input_data
        grade = int(gr)

        #перевірка чи є така дисципліна, якщо немає, то вивести повідомлення
        #raise Exception("There is no such discipline in your list. Add discipline /add_discipline")

        if grade_type not in ['p', 'l']:
            raise Exception("Invalid grade type. It must be either 'p' (practice) or 'l' (lecture).")

        if grade < 0 or grade > 100:
            raise Exception("Your grade must be between 0 and 100.")

        bot.reply_to(message, f"Grade {grade} for {discipline_name} ({grade_type}) submitted successfully!")

    except ValueError:
        bot.reply_to(message, "You entered an invalid grade. Please enter a numeric value between 0 and 100.")
        bot.register_next_step_handler(message, process_grade_input)
    except Exception as e:
        bot.reply_to(message, str(e))
        bot.register_next_step_handler(message, process_grade_input)


@bot.message_handler(commands=['remove_grade'])
def remove_grade_handler(message):
    bot.reply_to(message, "Please enter the discipline_name (use _ instead spaces)")
    bot.register_next_step_handler(message, discipline_to_remove_input)

def discipline_to_remove_input(message):
    try:
        command_list = message.text.split()
        if len(command_list) != 1:
            raise Exception("Invalid format. It must be like: discipline_name")

        discipline_name = command_list

        # перевірка чи є така дисципліна, якщо немає, то вивести повідомлення
        # raise Exception("There is no such discipline in your list. Add discipline /add_discipline")

        removed_gr=None
        #remove last from discip grades list
        #в повідомлення додати значення видаленого балу
        bot.reply_to(message, f"Grade {removed_gr} removed successfully!")

    except Exception as e:
        bot.reply_to(message, str(e))
        bot.register_next_step_handler(message, discipline_to_remove_input)


@bot.message_handler(commands=['show_grades_list'])
def show_grade_list_handler(message):
    bot.reply_to(message, "Please enter the discipline_name (use _ instead spaces)")
    bot.register_next_step_handler(message, discipline_to_show_list_input)

def discipline_to_show_list_input(message):
    try:
        command_list = message.text.split()
        if len(command_list) != 1:
            raise Exception("Invalid format. It must be like: discipline_name")

        discipline_name = command_list

        disc_grades_list=[1, 2, 3, 4]
        grades_list = ', '.join(map(str, disc_grades_list))

        # remove last from discip grades list
        # в повідомлення додати значення видаленого балу
        bot.reply_to(message, f"{discipline_name}: {grades_list} ")

    except Exception as e:
        bot.reply_to(message, str(e))
        bot.register_next_step_handler(message, discipline_to_show_list_input)


@bot.message_handler(commands=['add_discipline'])
def add_discipline(message):
    bot.reply_to(message, "Please enter the discipline_name (use _ instead spaces)")
    bot.register_next_step_handler(message, discipline_to_add_input)

def discipline_to_add_input(message):
    try:
        command_list = message.text.split()
        if len(command_list) != 1:
            raise Exception("Invalid format. It must be like: discipline_name")

        discipline_name = command_list

        discipline_names.append(discipline_name) #чи є вже така в списку

        bot.reply_to(message, f"Discipline '{discipline_name}' submitted successfully!")

    except Exception as e:
        bot.reply_to(message, str(e))
        bot.register_next_step_handler(message, discipline_to_add_input)


@bot.message_handler(commands=['remove_discipline'])
def remove_discipline(message):
    bot.reply_to(message, "Please enter the discipline_name (use _ instead spaces)")
    bot.register_next_step_handler(message, discipline_to_remove)

def discipline_to_remove(message):
    try:
        command_list = message.text.split()
        if len(command_list) != 1:
            raise Exception("Invalid format. It must be like: discipline_name")

        dis_name = command_list
        if dis_name not in discipline_names:
            raise Exception("The discipline is not listed")
        else:
            discipline_names.remove(dis_name)
            bot.reply_to(message, f"Discipline {dis_name} was removed successfully")
    except Exception as e:
        bot.reply_to(message, str(e))
        bot.register_next_step_handler(message, discipline_to_remove)

@bot.message_handler(commands=['all_disciplines'])
def show_disciplines_list(message):
    command_list = message.text.split()
    if len(command_list) != 1:
        raise Exception("Invalid format. It must be like: /all_disciplines")

    if len(disciplines) == 0:
        bot.reply_to(message, "Your discipline list is empty")
    else:
        bot.reply_to(message, str(disciplines))

@bot.message_handler(commands=['discipline_chart'])
def show_discipline_chart(message):
    bot.reply_to(message, "Please enter the discipline_name (use _ instead spaces)")
    bot.register_next_step_handler(message, discipline_to_shoe_chart)

def discipline_to_shoe_chart(message):
    try:
        command_list = message.text.split()
        if len(command_list) != 1:
            raise Exception("Invalid format. It must be like: discipline")

        dis_name = command_list
        if dis_name not in disciplines:
            raise Exception("The discipline is not listed")

        if len(disciplines) == 0:
            bot.reply_to(message, "You have no data to make chart")
        else:
            discip1 = dsc.Discipline(dis_name, 13, 43)
            ch = dsc.ChartMaker()
            ch.make_pie_chart(discip1)
            output_directory = f"{dis_name}_piechart.png"
            with open(output_directory, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)

    except Exception as e:
        bot.reply_to(message, str(e))
        bot.register_next_step_handler(message, discipline_to_shoe_chart)


if __name__ == "__main__":
    bot.infinity_polling()
