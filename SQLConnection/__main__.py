from SQLConnection.tests import db_module_tests

import sys
import unittest

IU_WARNING = "Usage: python -m SQLConnection test"

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(db_module_tests)
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
        else:
            print(IU_WARNING)
    else:
        print(IU_WARNING)

if __name__ == "__main__":
    main()
