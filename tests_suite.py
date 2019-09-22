import unittest

from tests.disk_management.test_suite_disk_read import test_suite_disk_read
from tests.install_queue.test_suite_event import test_suite_event

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(test_suite_disk_read())
    runner.run(test_suite_event())
