#runs every test in the tests folder with one command, the way a CI pipeline would.
#exits with code 1 if any test fails, so a pipeline (or Docker) can see the failure.
#run from the Lab-9 folder with: python run_tests.py
#same as: python -m unittest discover -s tests -t . -v

import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    suite = unittest.defaultTestLoader.discover(os.path.join(BASE_DIR, "tests"),
                                                top_level_dir=BASE_DIR)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
