
from gi.repository import Gtk

class BasePageGtk(Gtk.Box):
    """ Base widget for all page implementations to save on duplication. """

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=0)

        mk = u"<span font-size='x-large'>{}</span>".format("zizi")
        lab = Gtk.Label.new(mk)
        lab.set_property("margin-top", 10)
        lab.set_property("margin-start", 20)
        lab.set_property("margin-bottom", 10)
        lab.set_use_markup(True)
        lab.set_halign(Gtk.Align.START)
        self.pack_start(lab, False, False, 0)

        sep = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
        self.pack_start(sep, False, False, 0)

    def get_sidebar_title(self):
        return "Not implemented.."

    def get_name(self):
        return None

    def get_icon_name(self, plasma=False):
        return "dialog-error"

    def get_primary_answer(self):
        return None

    def prepare(self, info):
        pass

    def seed(self, setup):
        pass

    def is_hidden(self):
        return False

    def do_expensive_init(self):
        """ Do expensive startup tasks outside of the main thread """
        pass
