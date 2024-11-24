import unittest
import telebot
from unittest.mock import MagicMock, patch
from datetime import datetime

from grades_bot import bot, submit_grade_handler

class TestTelegramBot(unittest.TestCase):

    @patch('telebot.TeleBot.reply_to')
    def test_submit_grade_correct_value(self, mock_reply_to): #Тест для коректного значення
        message = MagicMock()
        message.text = "/submit_grade 50"

        submit_grade_handler(message)

        mock_reply_to.assert_called_once_with(message, "Grade 50 submitted successfully!")

    @patch('telebot.TeleBot.reply_to')
    def test_submit_grade_invalid_value(self, mock_reply_to):  # Тест для нечислового значення
        message = MagicMock()
        message.text = "/submit_grade abc"

        submit_grade_handler(message)

        mock_reply_to.assert_called_once_with(message, "You entered an invalid grade. Please enter a numeric value between 0 and 100.")

    @patch('telebot.TeleBot.reply_to')
    def test_submit_grade_invalid_format(self, mock_reply_to):  # Тест для некоректного формату
        message = MagicMock()
        message.text = "/submit_grade"

        submit_grade_handler(message)
        mock_reply_to.assert_called_once_with(message, "Invalid format. It must be like: /submit_grade grade")

    @patch('telebot.TeleBot.reply_to')
    def test_submit_grade_out_of_range_value(self, mock_reply_to):  #Тест для значення >100
        message = MagicMock()
        message.text = "/submit_grade 105"

        submit_grade_handler(message)

        mock_reply_to.assert_called_once_with(message, "Your grade must be between 0 and 100")

    @patch('telebot.TeleBot.reply_to')
    def test_submit_grade_negative_value(self, mock_reply_to):  #Тест для значення <0
        message = MagicMock()
        message.text = "/submit_grade -5"

        submit_grade_handler(message)

        mock_reply_to.assert_called_once_with(message, "Your grade must be between 0 and 100")

    @patch('telebot.TeleBot.reply_to')
    def test_submit_grade_correct_zero_value(self, mock_reply_to):  #Тест на перевірку 0
        message = MagicMock()
        message.text = "/submit_grade 0"

        submit_grade_handler(message)

        mock_reply_to.assert_called_once_with(message, "Grade 0 submitted successfully!")




if __name__ == '__main__':
   bot.infinity_polling()