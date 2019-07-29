from egg.app import App
from ui.gtk.containers import Windows
from ui.gtk.popup import PopupGtk


class GtkApp(App):
    def __init__(self):
        super(GtkApp, self).__init__()

    def display_popup(self, title, msg, popup_type):
        popup = PopupGtk(title, msg, popup_type)
        popup.launch()

    def launch(self):
        window = Windows.main_window_gtk()
        window.launch()
