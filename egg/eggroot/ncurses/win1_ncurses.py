from eggroot.interfaces.win1_interface import win1_interface

@win1_interface.register
class Win1_ncurses(win1_interface):
    def __init__(self, config, language_manager):
        pass
    
    def lunch(self):
        pass