import mysql.connector

class DBError(Exception):
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, self.message)

class SQLConnectionWrapper:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def user_exists(self, telegram_id):
        self.cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
        try:
            return self.cursor.fetchone() is not None
        except mysql.connector.Error as err:
            raise DBError(f"Error: {err}")

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

    def delete_user(self, telegram_id):
        if not self.user_exists(telegram_id):
            raise DBError(f"User with telegram id {telegram_id} does not exist")
        else:
            try:
                self.cursor.execute("DELETE FROM users WHERE telegram_id = %s", (telegram_id,))
                self.connection.commit()
            except mysql.connector.Error as err:
                raise DBError(f"Error: {err}")
