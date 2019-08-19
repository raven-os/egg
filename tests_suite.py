import unittest

from tests.disk_management.test_suite_disk_read import test_suite_disk_read

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(test_suite_disk_read())
