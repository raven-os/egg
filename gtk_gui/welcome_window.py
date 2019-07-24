import gi

from interfaces.welcome_window_interface import WelcomeWindowInterface

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, GObject, Gtk, GdkPixbuf


class Handler:
    @staticmethod
    def on_destroy(*args):
        Gtk.main_quit()


class Components():
    def __init__(self, builder):
        self._allComponents = {}
        self._builder = builder

    def load_component_main_window(self, config):
        for component_name in config["window_list_components"]:
            self._allComponents[component_name] = self._builder.get_object(component_name)

    def set_component(self, component_name, component):
        self._allComponents[component_name] = component

    def get_component(self, component_name):
        return self._allComponents[component_name]


@WelcomeWindowInterface.register
class WelcomeWindowGtk(WelcomeWindowInterface):

    def __init__(self, language_manager, config_general, config_main_window):
        GObject.threads_init()
        Gdk.threads_init()

        self._settings = Gtk.Settings.get_default()
        self._config_main_window = config_main_window
        self._config_general = config_general
        self._pages = list()
        self._page_index = 0
        self._lang_manager = language_manager
        self._builder = Gtk.Builder()
        self._builder.add_from_file(self._config_main_window["window_xml_file"])

        self._builder.connect_signals(
            {
                'onDestroy': Handler.on_destroy,
                'onButtonExit': Handler.on_destroy
            })
        self._component = Components(self._builder)

        self.init_window()
        self.set_full_screen_win()
        self.set_scroll_left()
        self.set_theme()
        self._component.get_component("welcome_window").show_all()

    def init_window(self):
        self._component.load_component_main_window(self._config_main_window)
        self._component.get_component("welcome_window").set_title(self._config_general["os_name"])
        self._component.get_component("welcome_window_left_bot_label").set_label("")
        pix_buf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self._config_main_window["window_logo_bot_path"],
                                                          180, 76, False)
        self._component.get_component("welcome_window_left_bot_logo").set_from_pixbuf(pix_buf)

    def set_full_screen_win(self):
        if self._config_main_window["window_fullscreen"]:
            self._component.get_component("welcome_window").fullscreen()

    def set_scroll_left(self):
        ltr = Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
        self._component.get_component("welcome_window_right_stack").set_transition_type(ltr)

    def set_theme(self):
        self._settings.set_property("gtk-application-prefer-dark-theme", True)

    def set_title(self, message):
        self._component.get_component("welcome_window_right_header_label").set_halign(Gtk.Align.START)
        self._component.get_component("welcome_window_right_header_label").set_label(
            u"<span font-size='x-large'>{}</span>".format(message))

    def launch(self):
        Gtk.main()
