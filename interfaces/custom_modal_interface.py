import abc


class CustomModalInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod 
    def launch(self, title, msg, event_type):
        pass
