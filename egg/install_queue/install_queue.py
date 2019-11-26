from collections import deque

from egg.install_queue.install_event import InstallEvent
from egg.singleton import Singleton


class InstallQueue(metaclass=Singleton):

    __queue = deque()

    def add(self, event: InstallEvent):
        self.__queue.append(event)

    def exec_left(self):
        self.__queue.popleft().exec()

    def exec_all(self):
        if len(self.__queue) > 0:
            self.exec_left()
            self.exec_all()
