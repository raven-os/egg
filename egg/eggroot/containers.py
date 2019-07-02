from dependency_injector import providers, containers

# general
from eggroot.general.language_management import LanguageManagement

# gtk
from eggroot.gtk.custom_modal_gtk import custom_modal_gtk
from eggroot.gtk.welcome_win_gtk import welcome_win_gtk

    # pages
from eggroot.gtk.pages.language_live_page_gtk import language_live_page_gtk
from eggroot.gtk.pages.language_installation_page_gtk import language_installation_page_gtk

# ncurses
from eggroot.ncurses.welcome_win_ncurses import welcome_win_ncurses

class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    config_main_window_page = providers.Configuration('config')
    # other configs

class Locales(containers.DeclarativeContainer):
    # use cfg for know default language
    locale_general = providers.Singleton(LanguageManagement, None, None, None)

class GraphicGui(containers.DeclarativeContainer):
    # GTK
    custom_modal_gtk = providers.Singleton(custom_modal_gtk)
    welcome_win_gtk = providers.Singleton(welcome_win_gtk, Locales.locale_general, Configs.config, Configs.config_main_window_page)
    language_live_page_gtk = providers.Factory(language_live_page_gtk, Locales.locale_general, Configs.config)
    language_installation_page_gtk = providers.Factory(language_installation_page_gtk, Locales.locale_general, Configs.config)


    welcome_win_ncurses = providers.Singleton(welcome_win_ncurses, Locales.locale_general, Configs.config, Configs.config_main_window_page)
    # custom_modal_ncurses = providers.Singleton(custom_modal_ncurses, Locales.locale_general)

    # other component gui