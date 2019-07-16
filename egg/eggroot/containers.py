from dependency_injector import providers, containers

# general
from eggroot.general.language_management import LanguageManagement

# gtk
from eggroot.gtk.custom_modal_gtk import CustomModalGtk

class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    config_main_window_page = providers.Configuration('config')

class Locales(containers.DeclarativeContainer):
    locale_general = providers.Singleton(LanguageManagement, None, None, None)

class GraphicGui(containers.DeclarativeContainer):
    custom_modal_gtk = providers.Singleton(CustomModalGtk)