import telebot

TOKEN = "7740781215:AAHKs_1YFhVueNbPbx93XreIH5WrpQANtrQ"
bot = telebot.TeleBot(TOKEN)


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


if __name__ == "__main__":
    bot.infinity_polling()
