from eggroot.gtk.pages.base_page_gtk import BasePageGtk
from eggroot.general.tz import Database

from gi.repository import TimezoneMap, Gtk, Gdk, GLib
import urllib.request
import geoip2.database
import json
import threading

class Components():
    _components = {}
    
    def __init__(self):
        self._components["frame_window"] = Gtk.Frame()
        self._components["tz_map"] = TimezoneMap.TimezoneMap()
        self._components["city_entry"] = Gtk.Entry()
        self._components["tz_completion"] = TimezoneMap.TimezoneCompletion()

    def get_component(self, component_name):
        return self._components[component_name]


class timezone_page_gtk(BasePageGtk):
    """ timezone setup page. """
    db = None
    timeout = 10
    _components = None

    def __init__(self, language_manager, config_general):
        BasePageGtk.__init__(self)

        self._language_manager = language_manager
        self._config_general = config_general
        self._components = Components()
        self._win_parent = None
        self._config_general["timezone_page"] = {}

        self.init_components()
        self.refresh_ui_language()

    def init_components(self):
        self._components.get_component("frame_window").set_shadow_type(Gtk.ShadowType.NONE)
        self.pack_start(self._components.get_component("frame_window"), True, True, 0)
        self._components.get_component("frame_window").set_margin_end(0)
        self._components.get_component("frame_window").set_margin_start(0)
        self._components.get_component("frame_window").add(self._components.get_component("tz_map"))

        self._components.get_component("city_entry").set_property("margin-right", 30)
        self._components.get_component("city_entry").set_property("margin-start", 30)
        self._components.get_component("city_entry").set_property("margin-top", 10)
        self.pack_end(self._components.get_component("city_entry"), False, False, 0)


        self._components.get_component("tz_completion").set_text_column(0)
        self._components.get_component("tz_completion").set_inline_completion(True)
        self._components.get_component("tz_completion").set_inline_selection(True)
        self._components.get_component("tz_completion").connect("match-selected", self.change_timezone)
        self._components.get_component("city_entry").set_completion(self._components.get_component("tz_completion"))
        self._components.get_component("tz_map").connect("location-changed", self.changed)

    def load_win(self, win):
        self._win_parent = win

    def refresh_ui_language(self):
        self._components.get_component("city_entry").set_placeholder_text(self._language_manager.print_in_lang("timezone_page", "timezone_placeholder_search_entry") + u"…")

    def do_expensive_init(self):
        # Set up timezone database
        self.db = Database()

        tz_model = Gtk.ListStore(str, str, str, str, float, float, str)

        for item in self.db.locations:
            tz_model.append([item.human_zone, item.human_country,  None,
                             item.country, item.longitude, item.latitude,
                             item.zone])

        Gdk.threads_enter()
        self._components.get_component("city_entry").get_completion().set_model(tz_model)
        Gdk.threads_leave()



    def change_timezone(self, completion, model, selection):
        item = model[selection]
        zone = item[6]
        self._components.get_component("tz_map").set_timezone(zone)

    def changed(self, map, location):
        zone = location.get_property("zone")
        nice_loc = self.db.tz_to_loc[zone]

        self.timezone_human = "{} ({})".format(nice_loc.human_zone,
                                               nice_loc.human_country)
        self._components.get_component("tz_map").set_watermark(self.timezone_human)
        self._components.get_component("city_entry").set_text(nice_loc.human_zone)

        self._win_parent.set_can_next(True)
        self._config_general["timezone_page"]["timezone_zone"] = zone
        self._config_general["timezone_page"]["timezone_country"] = location.get_property("country")

    def prepare(self):
        self.schedule_lookup()

        if "timezone_zone" in self._config_general["timezone_page"]:
            self._win_parent.set_can_next(True)
        else:
            # Use geoip
            if "timezone_zone" in self._config_general["timezone_page"]:
                self._components.get_component("tz_map").set_timezone(self._config_general["timezone_page"]["timezone_zone"])
                self.timezone = self._config_general["timezone_page"]["timezone_zone"]
                self._win_parent.set_can_next(True)
            else:
                self._win_parent.set_can_next(False)
    
    # geoip
    def schedule_lookup(self):
        self._win_parent.set_can_next(False)
        self._win_parent.set_can_previous(False)
        GLib.idle_add(self.begin_thread)

    def begin_thread(self):
        t = threading.Thread(target=self.perform_lookup)
        t.start()
        return False

    def get_ip_address(self):
        """ Get our external IP address for this machine """
        try:
            with urllib.request.urlopen(self._config_general["url_check_ip"], None, self.timeout) as response:
               contents = json.loads(response.read())
            return contents["ip"]
        except Exception as e:
            print(e)
        return None

    def perform_lookup(self):
        """ Perform the actual lookup """
        ip = str(self.get_ip_address())
        if not ip:
            self._win_parent.set_can_previous(True)
            return

        gi = geoip2.database.Reader(self._config_general["geo_ip_dat"])
        response = gi.city(ip)
        self._config_general["timezone_page"]["timezone_country"] = response.country.iso_code
        self._config_general["timezone_page"]["timezone_zone"] = response.location.time_zone
        self._components.get_component("tz_map").set_timezone(self._config_general["timezone_page"]["timezone_zone"])
        self._win_parent.set_can_previous(True)



    def get_title(self):
        return self._language_manager.print_in_lang("timezone_page", "title")

    def get_sidebar_title(self):
        return self._language_manager.print_in_lang("timezone_page", "sidebar_title")

    def get_name(self):
        return "timezone"

    def get_icon_name(self, plasma=False):
        return "preferences-system-time"