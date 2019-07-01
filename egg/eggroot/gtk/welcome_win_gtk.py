import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

from eggroot.interfaces.welcome_win_interface import welcome_win_interface

# pages
from eggroot.gtk.pages.language_live_page_gtk import language_live_page_gtk

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

    def onButtonPressed(self, button, *data):
        print("Hello World!")

    def onChangToFr(self, button, *data):
        data[1].change_language_all_files('fr')
        data[0].load_lang()

    def onChangToEn(self, button, *data):
        data[1].change_language_all_files('en')
        data[0].load_lang()

@welcome_win_interface.register
class welcome_win_gtk(welcome_win_interface):

   

    def __init__(self, config, language_manager):
        self._pages = list()
        self._page_index = 0
        self._lang_manager = language_manager
        self._lang_manager.change_language_all_files('fr')
        self._builder = Gtk.Builder()

        if __debug__:
            self._builder.add_from_file("/home/desaye_c/tek/egg/egg/eggroot/gtk/xml_gtk/welcome_win.glade")
        else:
            self._builder.add_from_file("./eggroot/gtk/xml_gtk/welcome_win.glade")

        self._builder.connect_signals(
            {
                'onButtonPressed': (Handler().onButtonPressed, language_manager),
                'onDestroy': (Handler().onDestroy),
                'onChangToFr': (Handler().onChangToFr, self, language_manager),
                'onChangToEn': (Handler().onChangToEn, self, language_manager)
            })

        allcomponents = self._builder.get_objects()
        self.init_window()
        self.load_lang()
        self.full_screen_win()
        self.set_scroll_left()
        self.set_theme()
        self.register_all_window()
        self.update_current_page()

        self._window.show_all()

    # init config
    def init_window(self):
        self._window = self._builder.get_object("welcome_win")
        self._nav_prev_btn = self._builder.get_object("welcome_win_prev_btn")
        self._nav_next_btn = self._builder.get_object("welcome_win_next_btn")
        self._left_top_icon = self._builder.get_object("welcome_win_left_top_logo")
        self._left_bot_icon = self._builder.get_object("welcome_win_left_bot_logo")

        self._window.set_title(self._lang_manager.print_in_lang('welcome_win', 'title'))
        self._left_label_box = self._builder.get_object("welcome_win_welcome_left_list_text_box")

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename="./img/raven_title_black.png", 
                width=24, 
                height=24, 
                preserve_aspect_ratio=True)


        self._left_bot_icon.new_from_pixbuf(pixbuf)

    def load_lang(self):
        pass
        # buttonclick = self._builder.get_object("button1")
        # buttonclick.set_label('click')
        
        # button_fr = self._builder.get_object("chang_fr")
        # button_fr.set_label(self._lang_manager.print_in_lang('welcome_win', 'lang_fr_button'))

        # button_us = self._builder.get_object("chang_en")
        # button_us.set_label(self._lang_manager.print_in_lang('welcome_win', 'lang_en_button'))

        # current_lang_label = self._builder.get_object("lang")
        # current_lang_label.set_label(self._lang_manager.print_in_lang('welcome_win', 'current_lang'))

    def full_screen_win(self):
        self._window.fullscreen()
        # self._window.hide()

    def set_scroll_left(self):
        ltr = Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
        self.installer_right_stack = self._builder.get_object("welcome_win_welcome_right_stack")
        self.installer_right_stack.set_transition_type(ltr)

    def set_theme(self):
        self._settings = Gtk.Settings.get_default()
        self._settings.set_property("gtk-application-prefer-dark-theme", True)

    def set_button_action(self):
        self._nav_prev_btn.connect("clicked", lambda x: self.prev_page())
        self._nav_next_btn.connect("clicked", lambda x: self.next_page())






    # manage other window
    def register_all_window(self):
        self.add_installer_page(language_live_page_gtk())
        self.add_installer_page(language_live_page_gtk())
        # self.add_installer_page(InstallerLocationPage())
        # self.add_installer_page(InstallerGeoipPage())
        # self.add_installer_page(InstallerKeyboardPage())
        # self.add_installer_page(InstallerTimezonePage())
        # self.add_installer_page(InstallerDiskLocationPage())
        # self.add_installer_page(InstallerPartitioningPage())
        # self.add_installer_page(InstallerSystemPage())
        # self.add_installer_page(InstallerUsersPage())
        # self.add_installer_page(InstallerSummaryPage(self.plasma))
        # self.add_installer_page(InstallerProgressPage())
        # self.add_installer_page(InstallationCompletePage())
















    def add_installer_page(self, page):
        """ Work a page into the set """
        self.installer_right_stack.add_named(page, page.get_name())
        lab = FancyLabel(page)
        self._left_label_box.pack_start(lab, False, False, 0)
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
        # page.prepare(self.info)

        for label in self._left_label_box.get_children():
            if label.page_id == page.get_name():
                label.get_style_context().remove_class("dim-label")
            else:
                label.get_style_context().add_class("dim-label")

        iname = page.get_icon_name()
        self._left_top_icon.set_from_icon_name(iname,
                                           Gtk.IconSize.DIALOG)
        self.installer_right_stack.set_visible_child_name(page.get_name())

    def set_can_previous(self, can_prev):
        self._nav_prev_btn.set_sensitive(can_prev)

    def set_can_next(self, can_next):
        self._nav_prev_btn.set_sensitive(can_next)

    def set_final_step(self, final):
        """ Mark this as the final step, should also
            add a prompt on selection """
        if final:
            self._nav_next_btn.set_label("Install")
        else:
            self._nav_next_btn.set_label("Next")
        self.is_final_step = final

    def set_can_quit(self, can_quit):
        """ Override quit handling """
        self.can_quit = can_quit
        if not self.can_quit:
            self._nav_prev_btn.hide()
            self._nav_next_btn.hide()
            # self.set_deletable(False)
        else:
            self._nav_prev_btn.show_all()
            self._nav_next_btn.show_all()
            # self.set_deletable(True)


    def _skip_page(self):
        """ Allow pages to request skipping to next page """
        if self.skip_forward:
            self.next_page()
        else:
            self.prev_page()
        return False

    def lunch(self):
        Gtk.main()