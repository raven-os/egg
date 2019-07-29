from dependency_injector import providers, containers
from egg.language_management import LanguageManagement


class Configs(containers.DeclarativeContainer):
    general = providers.Configuration('config')
    main_window = providers.Configuration('config')


class Locales(containers.DeclarativeContainer):
    locale_general = providers.Singleton(LanguageManagement)\
        .add_args(Configs.general, None)
