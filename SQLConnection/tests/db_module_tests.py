import datetime
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
        def remove_microseconds(dt):
            return dt.replace(microsecond=0)

        timestamp = remove_microseconds(datetime.datetime.now())

        self.connection.create_point(self.tg_id, "Math", PointType.LECTURE, 3, timestamp)
        self.connection.create_point(self.tg_id, "Math", PointType.LECTURE, 4, timestamp)
        self.connection.create_point(self.tg_id, "Math", PointType.PRACTICE, 5, timestamp)
        self.connection.create_point(self.tg_id, "Physics", PointType.LECTURE, 3, timestamp)
        self.connection.create_point(self.tg_id, "Physics", PointType.PRACTICE, 5, timestamp)
        self.connection.create_point(self.tg_id, "Physics", PointType.PRACTICE, 5, timestamp)

        data = self.connection.get_points_by_discipline(self.tg_id, "Math")
        expected = {
            "user_id": self.connection.get_user_by_telegram_id(self.tg_id)["id"],
            "discipline": "Math",
            "lecture_total_points": 50,
            "practice_total_points": 50,
            "points": {
                str(PointType.LECTURE): [{'value': 3, 'time': timestamp}, {'value': 4, 'time': timestamp}],
                str(PointType.PRACTICE): [{'value': 5, 'time': timestamp}]
            }
        }

        self.assertEqual(
            data,
            expected
        )

        data = self.connection.get_points_by_discipline(self.tg_id, "Physics")
        expected = {
            "user_id": self.connection.get_user_by_telegram_id(self.tg_id)["id"],
            "discipline": "Physics",
            "lecture_total_points": 50,
            "practice_total_points": 70,
            "points": {
                str(PointType.LECTURE): [{'value': 3, 'time': timestamp}],
                str(PointType.PRACTICE): [{'value': 5, 'time': timestamp}, {'value': 5, 'time': timestamp}]
            }
        }
        
        self.assertEqual(
            data,
            expected
        )

        start = timestamp - datetime.timedelta(days=1)
        end = timestamp + datetime.timedelta(days=1)

        data = self.connection.get_points_for_discipline_in_range(self.tg_id, "Physics", start, end)

        self.assertEqual(
            data,
            expected
        )


    def tearDown(self):
        self.connection.delete_user(self.tg_id)
        self.connection.__exit__(None, None, None)
