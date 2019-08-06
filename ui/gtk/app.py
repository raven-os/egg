from egg.app import App
from ui.gtk.containers import Windows
from ui.gtk.popup import PopupGtk
from egg.type_event import TypeEvent


class GtkApp(App):
    def __init__(self) -> None:
        super(GtkApp, self).__init__()

    def display_popup(self, title: str, msg: str, popup_type: TypeEvent) -> None:
        popup = PopupGtk(title, msg, popup_type)
        popup.launch()

    def launch(self) -> None:
        window = Windows.main_window_gtk()
        window.launch()
