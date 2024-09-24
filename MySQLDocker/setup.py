import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("MYSQL_ROOT_PASSWORD"),
)

user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
database = os.getenv("MYSQL_DATABASE")

cursor = connection.cursor()

# Create database if not exists
cursor.execute(f"SHOW DATABASES LIKE '{database}'")
if len(cursor.fetchall()) == 0:
    cursor.execute(f"CREATE DATABASE {database}")
    print("Database created successfully")
else:
    print("Database already exists")

# Use database
cursor.execute(f"USE {database}")

# Create user if not exists
cursor.execute(
    f"SELECT * FROM mysql.user WHERE user = '{user}' AND host = '%'"
)

if len(cursor.fetchall()) == 0:
    print("User does not exist")

    cursor.execute(
        f"CREATE USER IF NOT EXISTS {user}@'%' IDENTIFIED BY '{password}'"
    )

    print("User created successfully")
    cursor.execute(
        f"GRANT ALL PRIVILEGES ON {database}.* TO {user}@'%'"
    )
else:
    print("User already exists")

# Flush privileges
cursor.execute("FLUSH PRIVILEGES")

# Create users table
cursor.execute(f" \
    SELECT TABLE_NAME \
        FROM INFORMATION_SCHEMA.TABLES \
        WHERE TABLE_SCHEMA = '{database}' \
        AND TABLE_NAME = 'users' \
")

if len(cursor.fetchall()) == 0:
    print("Table does not exist")

    cursor.execute(" \
        CREATE TABLE IF NOT EXISTS users ( \
            id INT AUTO_INCREMENT PRIMARY KEY, \
            username VARCHAR(255) NOT NULL, \
            telegram_id INT UNSIGNED NOT NULL, \
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP \
        ) \
    ")
else:
    print("Table already exists")
