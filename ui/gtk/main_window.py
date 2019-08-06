import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gdk, GObject, Gtk, GdkPixbuf
from egg.language_management import LanguageManagement


class Handler:
    @staticmethod
    def on_destroy(widget: GObject.Object) -> None:
        Gtk.main_quit()


class Components:
    def __init__(self, builder: Gtk.Builder) -> None:
        self._all_components = {}
        self._builder = builder

    def load_component_main_window(self, config: dict) -> None:
        for component_name in config['window_list_components']:
            self._all_components[component_name] = self._builder.get_object(component_name)

    def set_component(self, component_name: str, component: GObject.Object) -> None:
        self._all_components[component_name] = component

    def get_component(self, component_name: str) -> None:
        return self._all_components[component_name]


class MainWindowGtk:

    def __init__(self, language_manager: LanguageManagement, config_general: dict, config_main_window: dict) -> None:
        GObject.threads_init()
        Gdk.threads_init()

        self._settings = Gtk.Settings.get_default()
        self._config_main_window = config_main_window
        self._config_general = config_general
        self._pages = list()
        self._page_index = 0
        self._lang_manager = language_manager
        self._builder = Gtk.Builder()
        self._builder.add_from_file(self._config_main_window['window_xml_file'])

        self._builder.connect_signals(
            {
                'onDestroy': Handler.on_destroy,
                'onButtonExit': Handler.on_destroy
            })
        self._component = Components(self._builder)

        self._component.load_component_main_window(self._config_main_window)
        self._component.get_component('main_window').set_default_size(int(self._config_main_window['window_size_x']),
                                                                      int(self._config_main_window['window_size_y']))
        self._component.get_component('main_window').set_title(self._config_general['os_name'])
        self._component.get_component('main_window_bot_left_label').set_label('')
        pix_buf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self._config_main_window['window_logo_bot_path'],
                                                          180, 76, False)
        self._component.get_component('main_window_bot_left_logo').set_from_pixbuf(pix_buf)
        if self._config_main_window['window_fullscreen']:
            self._component.get_component('main_window').fullscreen()
        ltr = Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
        self._component.get_component('main_window_right_stack').set_transition_type(ltr)
        self._settings.set_property('gtk-application-prefer-dark-theme', True)
        self._component.get_component('main_window').show_all()

    def set_title(self, message: str) -> None:
        self._component.get_component('main_window_header_right_label').set_halign(Gtk.Align.START)
        self._component.get_component('main_window_header_right_label').set_label(
            u'<span font-size=\'x-large\'>{}</span>'.format(message))

    def launch(self) -> None:
        Gtk.main()
