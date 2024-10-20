from SQLConnection.tests import connect_test

import sys
import unittest

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(connect_test)
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
        else:
            print("Usage: python -m SQLConnection test")
    else:
        print("Usage: python -m SQLConnection test")

if __name__ == "__main__":
    main()
