import SQLConnection
from SQLConnection.connection import SQLConnectionWrapper

import unittest

class TestUsersTable(unittest.TestCase):
    def setUp(self):
        self.connection = SQLConnectionWrapper("localhost", "GradesTracker", "GradesTracker", "GradesTracker")

    def test_user_exists(self):
        self.assertEqual(self.connection.user_exists("admin"), False)

    def tearDown(self):
        del self.connection
