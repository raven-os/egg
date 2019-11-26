from abc import ABC, abstractmethod
from enum import Enum


class InstallEvent(ABC):

    class EventType(Enum):
        TEST = 0
        DISK = 1
        PARTITION = 2

    def __init__(self, event_type: EventType, method_name: str, **kwargs):
        self.type = event_type
        self.method_name = method_name
        self.kwargs = kwargs

    @abstractmethod
    def exec(self):
        pass
