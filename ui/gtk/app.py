from egg.app import App
from egg.type_event import TypeEvent
from egg.language_management import LanguageManagement
from ui.gtk.popup import PopupGtk
from ui.gtk.main_window import MainWindowGtk


class GtkApp(App):
    def __init__(self, locale_general: LanguageManagement, config_general: dict, config_main_window: dict) -> None:
        super(GtkApp, self).__init__()
        self._locale_general = locale_general
        self._config_general = config_general
        self._config_main_window = config_main_window

    def display_popup(self, title: str, msg: str, popup_type: TypeEvent) -> None:
        popup = PopupGtk(title, msg, popup_type)
        popup.launch()

    def launch(self) -> None:
        window = MainWindowGtk(self._locale_general, self._config_general, self._config_main_window)
        window.launch()
