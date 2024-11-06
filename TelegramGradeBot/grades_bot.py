import telebot
from PngFormatter import discipline_statistics_charts as dsc

TOKEN="7227677197:AAEAJPpPqEdFICLGraX5kmnZ-77KuMYJZe4"
"""TOKEN = "7740781215:AAHKs_1YFhVueNbPbx93XreIH5WrpQANtrQ"""""
bot = telebot.TeleBot(TOKEN)

discipline_names=[]
disciplines={}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi, how are you doing")


@bot.message_handler(commands=['submit_grade'])
def submit_grade_handler(message):
    try:
        command_list = message.text.split()
        if len(command_list) != 2:
            raise Exception("Invalid format. It must be like: /submit_grade grade")

        command, gr = command_list
        grade = int(gr)

        if grade > 100 or grade < 0:
            raise Exception("Your grade must be between 0 and 100")
        else:
            bot.reply_to(message, f"Grade {grade} submitted successfully!")

    except ValueError:
        bot.reply_to(message, "You entered an invalid grade. Please enter a numeric value between 0 and 100.")
    except Exception as e:
        bot.reply_to(message, str(e))

@bot.message_handler(commands=['add_discipline'])
def add_discipline(message):
    try:
        command_list = message.text.split()
        if len(command_list) != 2:
            raise Exception("Invalid format. It must be like: /add_discipline discipline_name")

        command, dis_name = command_list
        discipline_name = dis_name

        if discipline_name not in discipline_names:
            discipline_names.append(discipline_name)
            bot.reply_to(message, f"Discipline '{discipline_name}' submitted successfully!")
            bot.reply_to(message, "Enter discipline's final type (credit, exam, project)")

            bot.register_next_step_handler(message, lambda msg: process_final_type(msg, discipline_name))
        else:
            raise Exception("This discipline is already in the list")
    except Exception as e:
        bot.reply_to(message, str(e))


def process_final_type(message, discipline_name):
    final_type = message.text.lower()
    if final_type not in ['credit', 'exam', 'project']:
        raise Exception("Invalid final type. Please enter one of the following: credit, exam, project")

    disciplines[discipline_name] = final_type
    bot.reply_to(message, f"Discipline '{discipline_name}' with final type '{final_type}' has been added successfully.")


@bot.message_handler(command=['remove_discipline'])
def remove_discipline(message):
    command_list = message.text.split()
    if len(command_list) != 2:
        raise Exception("Invalid format. It must be like: /remove_discipline discipline_name")
    command, dis_name = command_list
    if dis_name not in discipline_names:
        raise Exception("The discipline is not listed")
    else:
        discipline_names.remove(dis_name)
        bot.reply_to(message, f"Discipline {dis_name} was removed successfully")



@bot.message_handler(command=['all_disciplines'])
def show_disciplines_list(message):
    command_list = message.text.split()
    if len(command_list) != 1:
        raise Exception("Invalid format. It must be like: /all_disciplines")

    command = command_list

    bot.reply_to(disciplines)
    bot.reply_to("done!")

@bot.message_handler(command=['discipline_chart'])
def show_discipline_chart(message):
    command_list = message.text.split()
    if len(command_list) != 2:
        raise Exception("Invalid format. It must be like: /discipline_chart discipline")

    command, dis_name = command_list
    discip1 = dsc.Discipline(dis_name, 13, 43)
    ch=dsc.ChartMaker()
    ch.make_pie_chart(discip1)
    output_directory = f"{dis_name}_piechart.png"
    with open(output_directory, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


if __name__ == "__main__":
    bot.infinity_polling()
