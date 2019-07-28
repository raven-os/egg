from dependency_injector import providers, containers
from ui.gtk.main_window import MainWindowGtk
from egg.containers import Locales
from egg.containers import Configs


class Windows(containers.DeclarativeContainer):
    main_window_gtk = providers.Singleton(MainWindowGtk) \
        .add_args(Locales.locale_general, Configs.general, Configs.main_window)
