import abc

class CustomModalInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod 
    def lunch(self, title, msg, event_type):
        pass