from SQLConnection.connection import SQLConnectionWrapper

import unittest
import time
import os
from dotenv import load_dotenv

class TestUsersTable(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.connection = SQLConnectionWrapper(
            os.environ.get('SERVER'),
            os.environ.get('MYSQL_USER'),
            os.environ.get('MYSQL_PASSWORD'),
            os.environ.get('MYSQL_DATABASE')
        )

    def test_user_exists(self):
        self.assertFalse(self.connection.user_exists(time.time()))


    def test_create_user(self):
        tg_id = int(time.time())
        username = str(tg_id)
        self.connection.create_user(username, tg_id)
        self.assertTrue(self.connection.user_exists(tg_id))
        self.connection.delete_user(username)
        self.assertFalse(self.connection.user_exists(tg_id))

    def tearDown(self):
        del self.connection
