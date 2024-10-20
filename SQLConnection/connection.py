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

    def user_exists(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        return self.cursor.fetchone() is not None
