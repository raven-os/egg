import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from eggroot.general.type_event import type_event
from eggroot.interfaces.custom_modal_interface import custom_modal_interface

@custom_modal_interface.register
class custom_modal_gtk(custom_modal_interface):
    def __init__(self):
        pass

    def lunch(self, title, msg, event_type):
        gtk_type = None
        if event_type == type_event.INFO:
            gtk_type = Gtk.MessageType.INFO
        elif event_type == type_event.WARNING:
            gtk_type = Gtk.MessageType.WARNING
        elif event_type == type_event.ERROR:
            gtk_type = Gtk.MessageType.ERROR

        msg_popup = Gtk.MessageDialog(parent=None,
                            flags=Gtk.DialogFlags.MODAL,
                            type=gtk_type,
                            buttons=Gtk.ButtonsType.CLOSE,
                            message_format=msg,
                            title=title)
        msg_popup.run()
        msg_popup.destroy()