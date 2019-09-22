from collections import deque

from egg.install_queue.install_event import InstallEvent
from egg.singleton import Singleton


class InstallQueue(metaclass=Singleton):

    __queue = deque()

    def add(self, event: InstallEvent):
        self.__queue.append(event)

    def execLeft(self):
        self.__queue.popleft().exec()

    def execAll(self):
        if len(self.__queue) > 0:
            self.execLeft()
            self.execAll()
