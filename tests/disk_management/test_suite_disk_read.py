import unittest

from tests.disk_management import create_disk_test_case
from tests.disk_management.test_disk_read import TestDiskRead


def test_suite_disk_read():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    test_case = create_disk_test_case(testcase_type=TestDiskRead, scenario_data={'vhd_name': 'gpt_512M_4p'})
    suite.addTest(loader.loadTestsFromTestCase(test_case))
    return suite
