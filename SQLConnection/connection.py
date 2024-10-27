from typing import Any
import mysql.connector
from enum import Enum

class DBError(Exception):
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, self.message)

class PointType(Enum):
    LECTURE = 0
    PRACTICE = 1

    @staticmethod
    def from_string(string):
        if string == "lecture":
            return PointType.LECTURE
        elif string == "practice":
            return PointType.PRACTICE
        else:
            raise ValueError(f"Unknown point type: {string}")

    def __str__(self):
        if self == PointType.LECTURE:
            return "lecture"
        elif self == PointType.PRACTICE:
            return "practice"
        else:
            raise ValueError(f"Unknown point type: {self}")

class SQLConnectionWrapper:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


    def create_user(self, username, telegram_id):
        if self.user_exists(username):
            raise DBError(f"User {username} already exists")
        else:
            self.cursor.execute(
                "INSERT INTO users (username, telegram_id) VALUES (%s, %s)",
                (username, telegram_id)
            )
            try:
                self.connection.commit()
            except mysql.connector.Error as err:
                raise DBError(f"Error: {err}")


    def user_exists(self, telegram_id):
        self.cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
        try:
            return self.cursor.fetchone() is not None
        except mysql.connector.Error as err:
            raise DBError(f"Error: {err}")


    def get_user_by_telegram_id(self, telegram_id):
        if not self.user_exists(telegram_id):
            raise DBError(f"User with telegram_id {telegram_id} does not exist")

        self.cursor.execute("SELECt * FROM users WHERE telegram_id = %s", (telegram_id,))
        try:
            raw_user: Any = self.cursor.fetchone()
            return {
                "id": raw_user[0],
                "username": raw_user[1],
                "telegram_id": raw_user[2],
                "created_at": raw_user[3]
            }
        except mysql.connector.Error as err:
            raise DBError(f"Error: {err}")


    def delete_user(self, telegram_id):
        if not self.user_exists(telegram_id):
            raise DBError(f"User with telegram_id {telegram_id} does not exist")

        self.cursor.execute(
            "SELECT name FROM disciplines WHERE user_id = \
            (SELECT id FROM users WHERE telegram_id = %s)",
            (telegram_id,)
        )
        try:
            raw_disciplines: Any = self.cursor.fetchall()
            for raw_discipline in raw_disciplines:
                self.delete_discipline(telegram_id, raw_discipline[0])

            self.cursor.execute("DELETE FROM users WHERE telegram_id = %s", (telegram_id,))
            self.connection.commit()
        except mysql.connector.Error as err:
            raise DBError(f"Error: {err}")


    def create_discipline(self, telegram_id, discipline_name, lecture_total_points, practice_total_points):
        if self.discipline_exists(telegram_id, discipline_name):
            raise DBError(f"Discipline {discipline_name} already exists")

        user_id = self.get_user_by_telegram_id(telegram_id)["id"]
        self.cursor.execute(
            "INSERT INTO disciplines \
            (user_id, name, lecture_total_points, practice_total_points) \
            VALUES (%s, %s, %s, %s)",
            (user_id, discipline_name, lecture_total_points, practice_total_points)
        )
        try:
            self.connection.commit()
        except mysql.connector.Error as err:
            raise DBError(f"Error: {err}")


    def discipline_exists(self, telegram_id, discipline_name):
        user_id = self.get_user_by_telegram_id(telegram_id)["id"]
        self.cursor.execute(
            "SELECT * FROM disciplines WHERE user_id = %s AND name = %s",
            (user_id, discipline_name)
        )
        try:
            return self.cursor.fetchone() is not None
        except mysql.connector.Error as err:
            raise DBError(f"Error: {err}")


    def get_discipline_by_name(self, telegram_id, discipline_name):
        if not self.discipline_exists(telegram_id, discipline_name):
            raise DBError(f"Discipline {discipline_name} does not exist")

        user_id = self.get_user_by_telegram_id(telegram_id)["id"]
        self.cursor.execute(
            "SELECT * FROM disciplines WHERE user_id = %s AND name = %s",
            (user_id, discipline_name)
        )
        try:
            raw_discipline: Any = self.cursor.fetchone()
            return {
                "id": raw_discipline[0],
                "user_id": raw_discipline[1],
                "name": raw_discipline[2],
                "lecture_total_points": raw_discipline[3],
                "practice_total_points": raw_discipline[4]
            }
        except mysql.connector.Error as err:
            raise DBError(f"Error: {err}")


    def delete_discipline(self, telegram_id, discipline_name):
        if not self.discipline_exists(telegram_id, discipline_name):
            raise DBError(f"Discipline {discipline_name} does not exist")

        user_id = self.get_user_by_telegram_id(telegram_id)["id"]
        self.cursor.execute(
            "DELETE FROM points WHERE discipline_id = \
            (SELECT id FROM disciplines WHERE user_id = %s AND name = %s)",
            (user_id, discipline_name)
        )
        self.cursor.execute(
            "DELETE FROM disciplines WHERE user_id = %s AND name = %s",
            (user_id, discipline_name)
        )
        try:
            self.connection.commit()
        except mysql.connector.Error as err:
            raise DBError(f"Error: {err}")


    def create_point(self, telegram_id, discipline_name, point_type: PointType, points):
        discipline_id = self.get_discipline_by_name(telegram_id, discipline_name)["id"]
        self.cursor.execute(
            "INSERT INTO points (discipline_id, type, points) VALUES (%s, %s, %s)",
            (discipline_id, str(point_type), points)
        )
        try:
            self.connection.commit()
        except mysql.connector.Error as err:
            raise DBError(f"Error: {err}")


    def get_points_by_discipline(self, telegram_id, discipline_name):
        user = self.get_user_by_telegram_id(telegram_id)
        discipline = self.get_discipline_by_name(telegram_id, discipline_name)

        self.cursor.execute(
            "SELECT type, points \
            FROM disciplines \
            JOIN points ON disciplines.id = points.discipline_id \
            WHERE user_id = %s AND name = %s",
            (user["id"], discipline_name)
        )
        try:
            raw_points: Any = self.cursor.fetchall()
            return {
                "user_id": user["id"],
                "discipline": discipline_name,
                "lecture_total_points": discipline["lecture_total_points"],
                "practice_total_points": discipline["practice_total_points"],
                "points": {
                    str(PointType.LECTURE): [raw_point[1] for raw_point in raw_points if raw_point[0] == "lecture"],
                    str(PointType.PRACTICE): [raw_point[1] for raw_point in raw_points if raw_point[0] == "practice"]
                }
            }
        except mysql.connector.Error as err:
            raise DBError(f"Error: {err}")
