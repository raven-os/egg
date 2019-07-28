import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from egg.type_event import TypeEvent


class PopupGtk:

    def __init__(self, title, msg, event_type):
        self._title = title
        self._msg = msg
        self._event_type = event_type

    def launch(self):
        gtk_type = Gtk.MessageType.OTHER

        if self._event_type == TypeEvent.INFO:
            gtk_type = Gtk.MessageType.INFO
        elif self._event_type == TypeEvent.WARNING:
            gtk_type = Gtk.MessageType.WARNING
        elif self._event_type == TypeEvent.ERROR:
            gtk_type = Gtk.MessageType.ERROR

        msg_popup = Gtk.MessageDialog(parent=None,
                                      flags=Gtk.DialogFlags.MODAL,
                                      type=gtk_type,
                                      buttons=Gtk.ButtonsType.CLOSE,
                                      message_format=self._msg,
                                      title=self._title)
        msg_popup.run()
        msg_popup.destroy()
