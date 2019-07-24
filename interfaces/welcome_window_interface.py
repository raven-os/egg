import abc


class WelcomeWindowInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod 
    def launch(self):
        pass
