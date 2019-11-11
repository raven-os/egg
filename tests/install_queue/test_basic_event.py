import unittest

from egg.install_queue.install_event import InstallEvent
from egg.install_queue.install_queue import InstallQueue
from tests import captured_output


class BasicTestClass(object):
    def __init__(self, method_name: str):
        self.method_name = method_name

    def print_test(self, value: int):
        print('method_name: %s, value: %s' % (self.method_name, value))


class BasicEvent(InstallEvent):

    def __init__(self, method_name: str, **kwargs):
        super().__init__(InstallEvent.EventType.TEST, method_name, **kwargs)

    def exec(self):
        basic_instance = BasicTestClass(self.method_name)
        getattr(basic_instance, self.method_name)(**self.kwargs)


class TestBasicEvent(unittest.TestCase):

    def test_basic_event(self):
        event = BasicEvent(BasicTestClass.print_test.__name__, value=1)
        InstallQueue().add(event)
        with captured_output() as (out, err):
            InstallQueue().execAll()
        output = out.getvalue().strip()
        self.assertEqual(output, 'method_name: print_test, value: 1')
