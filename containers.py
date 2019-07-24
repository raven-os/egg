from dependency_injector import providers, containers

# services
from services.language_management import LanguageManagement

# gtk
from gtk_gui.custom_modal import CustomModalGtk
from gtk_gui.welcome_window import WelcomeWindowGtk


class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    config_main_window_page = providers.Configuration('config')


class Locales(containers.DeclarativeContainer):
    locale_general = providers.Singleton(LanguageManagement, None, None, None)


class GraphicGui(containers.DeclarativeContainer):
    custom_modal_gtk = providers.Singleton(CustomModalGtk)
    welcome_window_gtk = providers.Singleton(WelcomeWindowGtk, Locales.locale_general,
                                             Configs.config, Configs.config_main_window_page)
