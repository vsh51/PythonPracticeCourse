from SQLConnection.connection import SQLConnectionWrapper, PointType

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
        ).__enter__()


    def test_user_exists(self):
        self.assertFalse(self.connection.user_exists(time.time()))


    def test_create_user(self):
        tg_id = int(time.time())
        username = str(tg_id)
        self.connection.create_user(username, tg_id)
        self.assertTrue(self.connection.user_exists(tg_id))
        self.connection.delete_user(tg_id)
        self.assertFalse(self.connection.user_exists(tg_id))


    def tearDown(self):
        self.connection.__exit__(None, None, None)


class TestDisciplinesTable(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.connection = SQLConnectionWrapper(
            os.environ.get('SERVER'),
            os.environ.get('MYSQL_USER'),
            os.environ.get('MYSQL_PASSWORD'),
            os.environ.get('MYSQL_DATABASE')
        ).__enter__()


    def test_create_discipline(self):
        tg_id = int(time.time())
        username = str(tg_id)
        self.connection.create_user(username, tg_id)
        self.connection.create_discipline(tg_id, "Math", 50, 50)
        self.assertTrue(self.connection.discipline_exists(tg_id, "Math"))
        self.connection.delete_user(tg_id)


    def tearDown(self):
        self.connection.__exit__(None, None, None)


class TestPointsTable(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.connection = SQLConnectionWrapper(
            os.environ.get('SERVER'),
            os.environ.get('MYSQL_USER'),
            os.environ.get('MYSQL_PASSWORD'),
            os.environ.get('MYSQL_DATABASE')
        ).__enter__()

        self.tg_id = int(time.time())
        self.username = str(self.tg_id)
        self.connection.create_user(self.username, self.tg_id)
        self.connection.create_discipline(self.tg_id, "Math", 50, 50)
        self.connection.create_discipline(self.tg_id, "Physics", 50, 70)
        self.assertTrue(self.connection.discipline_exists(self.tg_id, "Physics"))
        self.assertTrue(self.connection.discipline_exists(self.tg_id, "Math"))


    def test_create_multiple_points(self):
        self.connection.create_point(self.tg_id, "Math", PointType.LECTURE, 3)
        self.connection.create_point(self.tg_id, "Math", PointType.LECTURE, 4)
        self.connection.create_point(self.tg_id, "Math", PointType.PRACTICE, 5)
        self.connection.create_point(self.tg_id, "Physics", PointType.LECTURE, 3)
        self.connection.create_point(self.tg_id, "Physics", PointType.PRACTICE, 5)
        self.connection.create_point(self.tg_id, "Physics", PointType.PRACTICE, 5)
        self.assertEqual(
            self.connection.get_points_by_discipline(self.tg_id, "Math"),
            {
                "user_id": self.connection.get_user_by_telegram_id(self.tg_id)["id"],
                "discipline": "Math",
                "lecture_total_points": 50,
                "practice_total_points": 50,
                "points": {
                    str(PointType.LECTURE): [3, 4],
                    str(PointType.PRACTICE): [5]
                }
            }
        )
        self.assertEqual(
            self.connection.get_points_by_discipline(self.tg_id, "Physics"),
            {
                "user_id": self.connection.get_user_by_telegram_id(self.tg_id)["id"],
                "discipline": "Physics",
                "lecture_total_points": 50,
                "practice_total_points": 70,
                "points": {
                    str(PointType.LECTURE): [3],
                    str(PointType.PRACTICE): [5, 5]
                }
            }
        )


    def tearDown(self):
        self.connection.delete_user(self.tg_id)
        self.connection.__exit__(None, None, None)
