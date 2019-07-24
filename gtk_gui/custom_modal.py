import gi
from gi.repository import Gtk
from events.type_event import TypeEvent
from interfaces.custom_modal_interface import CustomModalInterface
gi.require_version('Gtk', '3.0')


@CustomModalInterface.register
class CustomModalGtk(CustomModalInterface):
    def __init__(self):
        pass

    def launch(self, title, msg, event_type):
        gtk_type = Gtk.MessageType.OTHER

        if event_type == TypeEvent.INFO:
            gtk_type = Gtk.MessageType.INFO
        elif event_type == TypeEvent.WARNING:
            gtk_type = Gtk.MessageType.WARNING
        elif event_type == TypeEvent.ERROR:
            gtk_type = Gtk.MessageType.ERROR

        msg_popup = Gtk.MessageDialog(parent=None,
                                      flags=Gtk.DialogFlags.MODAL,
                                      type=gtk_type,
                                      buttons=Gtk.ButtonsType.CLOSE,
                                      message_format=msg,
                                      title=title)
        msg_popup.run()
        msg_popup.destroy()
