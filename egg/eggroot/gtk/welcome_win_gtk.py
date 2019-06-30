import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from eggroot.interfaces.welcome_win_interface import welcome_win_interface

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
        self.load_lang()
        self.full_screen_win()
        self._window.show_all()
    
    def load_lang(self):
        self._window = self._builder.get_object("welcome_win")
        self._window.set_title(self._lang_manager.print_in_lang('welcome_win', 'title'))

        buttonclick = self._builder.get_object("button1")
        buttonclick.set_label('click')
        
        button_fr = self._builder.get_object("chang_fr")
        button_fr.set_label(self._lang_manager.print_in_lang('welcome_win', 'lang_fr_button'))
        

        button_us = self._builder.get_object("chang_en")
        button_us.set_label(self._lang_manager.print_in_lang('welcome_win', 'lang_en_button'))


        current_lang_label = self._builder.get_object("lang")
        current_lang_label.set_label(self._lang_manager.print_in_lang('welcome_win', 'current_lang'))

    def full_screen_win(self):
        self._window.fullscreen()
        # self._window.hide()

    def lunch(self):
        Gtk.main()