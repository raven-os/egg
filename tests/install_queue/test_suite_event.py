import unittest

from tests.install_queue.test_basic_event import TestBasicEvent


def test_suite_event():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(TestBasicEvent))
    return suite
