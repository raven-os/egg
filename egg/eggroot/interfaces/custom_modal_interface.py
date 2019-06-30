import abc

class custom_modal_interface(metaclass=abc.ABCMeta):
    @abc.abstractmethod 
    def lunch(self, title, msg, event_type):
        pass