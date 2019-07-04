
from gi.repository import Gtk

class BasePageGtk(Gtk.Box):
    """ Base widget for all page implementations to save on duplication. """

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=0)

    def refresh_ui_language(self):
        pass

    def load_win(self, win):
        pass

    def get_title(self):
        return None

    def get_sidebar_title(self):
        return "Not implemented.."

    def get_name(self):
        return None

    def get_icon_name(self, plasma=False):
        return "dialog-error"

    def get_primary_answer(self):
        return None

    def prepare(self):
        pass

    def seed(self, setup):
        pass

    def is_hidden(self):
        return False

    def do_expensive_init(self):
        """ Do expensive startup tasks outside of the main thread """
        pass
