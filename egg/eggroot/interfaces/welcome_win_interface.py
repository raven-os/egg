import abc

class welcome_win_interface(metaclass=abc.ABCMeta):
    @abc.abstractmethod 
    def lunch(self):
        pass