from eggroot.interfaces.welcome_win_interface import welcome_win_interface

@welcome_win_interface.register
class welcome_win_ncurses(welcome_win_interface):
    def __init__(self, config, language_manager):
        pass
    
    def lunch(self):
        pass