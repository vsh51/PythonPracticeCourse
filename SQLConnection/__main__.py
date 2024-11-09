from SQLConnection.tests import db_module_tests
from SQLConnection import SQLConnectionWrapper

import sys
import unittest
import os
from dotenv import load_dotenv

IU_WARNING = "Usage: python -m SQLConnection test"

def main():
    load_dotenv()

    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(db_module_tests)
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
        elif sys.argv[1] == "wipe":
            print("Wiping the database...")
            with SQLConnectionWrapper(os.environ.get('SERVER'), os.environ.get('MYSQL_USER'),
                            os.environ.get('MYSQL_PASSWORD'), os.environ.get('MYSQL_DATABASE')) as connection:
                connection.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                print("Setting foreign key checks to 0...")
                connection.cursor.execute("DELETE FROM users")
                print("Deleting users...")
                connection.cursor.execute("DELETE FROM disciplines")
                print("Deleting disciplines...")
                connection.cursor.execute("DELETE FROM points")
                print("Deleting points...")
                connection.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                print("Setting foreign key checks to 1...")
                connection.connection.commit()
            print("Database wiped")
        else:
            print(IU_WARNING)
    else:
        print(IU_WARNING)

if __name__ == "__main__":
    main()
