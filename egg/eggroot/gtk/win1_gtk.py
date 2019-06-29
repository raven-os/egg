import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from eggroot.interfaces.win1_interface import win1_interface

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

@win1_interface.register
class Win1_gtk(win1_interface):
    def __init__(self, config, language_manager):
        self._lang_manager = language_manager
        self._lang_manager.change_language_all_files('fr')
        self._builder = Gtk.Builder()

        if __debug__:
            self._builder.add_from_file("/home/desaye_c/tek/egg/egg/eggroot/gtk/builder_example.glade")
        else:
            self._builder.add_from_file("./eggroot/gtk/builder_example.glade")

        self._builder.connect_signals(
            {
                'onDestroy': (Handler().onDestroy),
                'onButtonPressed': (Handler().onButtonPressed, language_manager),
                'onChangToFr': (Handler().onChangToFr, self, language_manager),
                'onChangToEn': (Handler().onChangToEn, self, language_manager)
            })

        allcomponents = self._builder.get_objects()
        self.load_lang()
        self._window.show_all()
    
    def load_lang(self):
        self._window = self._builder.get_object("window1")
        self._window.set_title(self._lang_manager.print_in_lang('win1', 'title'))

        buttonclick = self._builder.get_object("button1")
        buttonclick.set_label('click')
        
        button_fr = self._builder.get_object("chang_fr")
        button_fr.set_label(self._lang_manager.print_in_lang('win1', 'lang_fr_button'))
        

        button_us = self._builder.get_object("chang_en")
        button_us.set_label(self._lang_manager.print_in_lang('win1', 'lang_en_button'))


        current_lang_label = self._builder.get_object("lang")
        current_lang_label.set_label(self._lang_manager.print_in_lang('win1', 'current_lang'))

    def lunch(self):
        Gtk.main()