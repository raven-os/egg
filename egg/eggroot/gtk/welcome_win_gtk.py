import eggroot.containers
import threading
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, GObject, Gtk, GLib, GdkPixbuf

from eggroot.interfaces.welcome_win_interface import welcome_win_interface

# pages
from eggroot.gtk.pages.language_live_page_gtk import language_live_page_gtk
from eggroot.gtk.pages.language_installation_page_gtk import language_installation_page_gtk

# select_row
class FancyLabel(Gtk.Label):

    page_id = None

    def __init__(self, page):
        Gtk.Label.__init__(self)
        self.set_label(page.get_sidebar_title())
        self.page_id = page.get_name()
        self.set_halign(Gtk.Align.START)
        self.set_property("margin", 6)
        self.set_property("margin-start", 24)
        self.set_property("margin-end", 24)
        self.get_style_context().add_class("dim-label")

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

class Components():
    def __init__(self, builder):
        self._allComponents = {}
        self._builder = builder

    def load_component_main_window(self, config):
        # put in config and for
        for component_name in config["window_list_components"]:
            self._allComponents[component_name] = self._builder.get_object(component_name)

    def set_component(self, component_name, component):
        self._allComponents[component_name] = component

    def get_component(self, component_name):
        return self._allComponents[component_name]

@welcome_win_interface.register
class welcome_win_gtk(welcome_win_interface):

    def __init__(self, language_manager, config_general, config_main_window):
        GObject.threads_init()
        Gdk.threads_init()

        self._config_main_window = config_main_window
        self._config_general = config_general
        self._pages = list()
        self._page_index = 0
        self._lang_manager = language_manager
        self._builder = Gtk.Builder()
        self._builder.add_from_file(self._config_main_window["window_xml_file"])

        self._builder.connect_signals(
        {
            'onDestroy': (Handler().onDestroy),
            'onButtonExit': (Handler().onDestroy)
        })

        # allcomponents = self._builder.get_objects()
        self.init_window()
        self.set_full_screen_win()
        self.set_scroll_left()
        self.set_theme()
        self.register_all_window()
        self.load_lang()
        self.update_current_page()
        self.set_button_action()
        self._component.get_component("welcome_win").show_all()
       
        GLib.idle_add(self.start_threads)

    # init config
    def init_window(self):
        self._component = Components(self._builder)
        self._component.load_component_main_window(self._config_main_window)
        self._component.get_component("welcome_win").set_title(self._config_general["os_name"])
        self._component.get_component("welcome_win_left_bot_label").set_label("")
        self._component.get_component("welcome_win_left_bot_logo").set_from_file(self._config_main_window["window_logo_bot_path"])

    def set_full_screen_win(self):
        if self._config_main_window["window_fullscreen"]:
            self._component.get_component("welcome_win").fullscreen()
            # self._window.hide()

    def set_scroll_left(self):
        ltr = Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
        self._component.get_component("welcome_win_welcome_right_stack").set_transition_type(ltr)

    def set_theme(self):
        self._settings = Gtk.Settings.get_default()
        self._settings.set_property("gtk-application-prefer-dark-theme", True)

    def set_button_action(self):
        # checker ici mettre dans la classe handler
        self._component.get_component("welcome_win_prev_btn").connect("clicked", lambda x: self.prev_page())
        self._component.get_component("welcome_win_next_btn").connect("clicked", lambda x: self.next_page())

    def set_title(self, message):
        self._component.get_component("welcome_win_welcome_right_header_label").set_halign(Gtk.Align.START)
        mk = u"<span font-size='x-large'>{}</span>".format(message)
        self._component.get_component("welcome_win_welcome_right_header_label").set_label(mk)
        
    # manage other window
    def register_all_window(self):
        all_pages = list()

        all_pages.append(eggroot.containers.GraphicGui.language_live_page_gtk())
        all_pages.append(eggroot.containers.GraphicGui.language_installation_page_gtk())
        all_pages.append(eggroot.containers.GraphicGui.timezone_page_gtk())
        for current_page in all_pages:
            current_page.load_win(self)
            self.add_installer_page(current_page)

    def load_lang(self):
        component = self._component.get_component("welcome_win_welcome_left_list_text_box")
        for label in component.get_children():
            component.remove(label)

        for current_page in self._pages:
            lab = FancyLabel(current_page)
            if lab.page_id == self._pages[self._page_index].get_name():
                lab.get_style_context().remove_class("dim-label")
            else:
                lab.get_style_context().add_class("dim-label")
            self._component.get_component("welcome_win_welcome_left_list_text_box").pack_start(lab, False, False, 0)
            current_page.refresh_ui_language()
        self._component.get_component("welcome_win_welcome_left_list_text_box").show_all()
        
        self.set_title(self._pages[self._page_index].get_title())
        self._component.get_component("welcome_win_welcome_right_header_quit_btn").set_label(self._lang_manager.print_in_lang('welcome_win', 'top_right_quit_btn'))
        self._component.get_component("welcome_win_prev_btn").set_label(self._lang_manager.print_in_lang('welcome_win', 'bot_right_prev_btn'))

        component = self._component.get_component("welcome_win_next_btn")
        component.set_label(self._lang_manager.print_in_lang('welcome_win', 'bot_right_next_btn'))

    def add_installer_page(self, page):
        """ Work a page into the set """
        self._component.get_component("welcome_win_welcome_right_stack").add_named(page, page.get_name())
        lab = FancyLabel(page)
        self._component.get_component("welcome_win_welcome_left_list_text_box").pack_start(lab, False, False, 0)
        self._pages.append(page)

    def next_page(self):
        """ Move to next page """
        if self.is_final_step:
            msg = "Installation will make changes to your disks, and could " \
                  "result in data loss.\nDo you wish to install?"
            d = Gtk.MessageDialog(parent=self, flags=Gtk.DialogFlags.MODAL,
                                  type=Gtk.MessageType.WARNING,
                                  buttons=Gtk.ButtonsType.OK_CANCEL,
                                  message_format=msg)

            r = d.run()
            d.destroy()
            if r != Gtk.ResponseType.OK:
                return

        self.skip_forward = True
        index = self._page_index + 1
        if index >= len(self._pages):
            return
        page = self._pages[index]
        if page.is_hidden():
            index += 1
        self._page_index = index
        self.update_current_page()

    def prev_page(self):
        self.skip_forward = False
        """ Move to previous page """
        index = self._page_index - 1
        if index < 0:
            return
        page = self._pages[index]
        if page.is_hidden():
            index -= 1
        self._page_index = index
        self.update_current_page()

    def update_current_page(self):
        self.set_title(self._pages[self._page_index].get_title())
        page = self._pages[self._page_index]
        self.set_final_step(False)

        if self._page_index == len(self._pages) - 1:
            self.set_can_next(False)
        else:
            self.set_can_next(True)
        if self._page_index == 0:
            self.set_can_previous(False)
        else:
            self.set_can_previous(True)

        # HERE Envoie d'info mais vide donc changer dans installationpage avec configloader
        page.prepare()

        for label in self._component.get_component("welcome_win_welcome_left_list_text_box").get_children():
            if label.page_id == page.get_name():
                label.get_style_context().remove_class("dim-label")
            else:
                label.get_style_context().add_class("dim-label")

        iname = page.get_icon_name()
        self._component.get_component("welcome_win_left_top_logo").set_from_icon_name(iname,
            Gtk.IconSize.DIALOG)
        self._component.get_component("welcome_win_welcome_right_stack").set_visible_child_name(page.get_name())

    def set_can_previous(self, can_prev):
        if self._page_index == 0:
            can_prev = False
        self._component.get_component("welcome_win_prev_btn").set_sensitive(can_prev)

    def set_can_next(self, can_next):
        if self._page_index == len(self._pages) - 1:
            can_next = False
        self._component.get_component("welcome_win_next_btn").set_sensitive(can_next)

    def set_final_step(self, final):
        """ Mark this as the final step, should also
            add a prompt on selection """
        if final:
            self._component.get_component("welcome_win_next_btn").set_label("Install")
        else:
            self._component.get_component("welcome_win_next_btn").set_label("Next")
        self.is_final_step = final

    def set_can_quit(self, can_quit):
        """ Override quit handling """
        self.can_quit = can_quit
        if not self.can_quit:
            self._component.get_component("welcome_win_prev_btn").hide()
            self._component.get_component("welcome_win_next_btn").hide()
            # self.set_deletable(False)
        else:
            self._component.get_component("welcome_win_prev_btn").show_all()
            self._component.get_component("welcome_win_next_btn").show_all()
            # self.set_deletable(True)

    def skip_page(self):
        GLib.idle_add(self._skip_page)

    def _skip_page(self):
        """ Allow pages to request skipping to next page """
        if self.skip_forward:
            self.next_page()
        else:
            self.prev_page()
        return False

    def perform_inits(self):
        """ Force expensive children to init outside main thread """
        # here expensive task load window
        for page in self._pages:
            try:
                page.do_expensive_init()
            except Exception as e:
                print("Fatal exception initialising: {}".format(e))

    def start_threads(self):
        self.set_can_next(False)
        start_thr = threading.Thread(target=self.perform_inits)
        start_thr.daemon = True
        start_thr.start()
        return False

    def lunch(self):
        Gtk.main()