from dependency_injector import providers, containers

# general
from eggroot.general.language_management import LanguageManagement

# gtk
from eggroot.gtk.custom_modal_gtk import custom_modal_gtk
from eggroot.gtk.welcome_win_gtk import welcome_win_gtk

# ncurses
from eggroot.ncurses.welcome_win_ncurses import welcome_win_ncurses

class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    # other configs

class Locales(containers.DeclarativeContainer):
    locale_general = providers.Singleton(LanguageManagement, 'fr', None)


class GraphicGui(containers.DeclarativeContainer):
    custom_modal_gtk = providers.Singleton(custom_modal_gtk)
    # custom_modal_ncurses = providers.Singleton(custom_modal_ncurses, Locales.locale_general)
    welcome_win_gtk = providers.Singleton(welcome_win_gtk, Configs.config, Locales.locale_general)
    welcome_win_ncurses = providers.Singleton(welcome_win_ncurses, Configs.config, Locales.locale_general)

    # other component gui