from dependency_injector import providers, containers
from eggroot.gtk.win1_gtk import Win1_gtk
from eggroot.ncurses.win1_ncurses import Win1_ncurses
from eggroot.general.language_management import LanguageManagement

class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    # other configs
    
class Clients(containers.DeclarativeContainer):
    locale_file1_fr = providers.Factory(LanguageManagement, 'fr', 'win1')
    locale_file1_us = providers.Factory(LanguageManagement, 'us', 'win1')
    
    win_gtk = providers.Singleton(Win1_gtk, Configs.config, locale_file1_fr)
    win_ncurses = providers.Singleton(Win1_ncurses, Configs.config, locale_file1_fr)
    # other clients