from eggroot.gtk.pages.base_page_gtk import BasePageGtk
from gi.repository import Gtk, GnomeDesktop, Gdk

import subprocess

default_locales = [
    "en_US.UTF-8",
    "de_DE.UTF-8",
    "fr_FR.UTF-8",
    "es_ES.UTF-8",
    "zh_CN.UTF-8",
    "ja_JP.UTF-8",
    "ru_RU.UTF-8",
    "ar_EG.UTF-8"
]

class KbLabel(Gtk.Box):
    """ View label for locales, save code duping """
    kb = None
    dname = None

    def __init__(self, kb, info):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        
        self.kb = kb
        lab = Gtk.Label("")
        lab.set_halign(Gtk.Align.START)

        self.dname = info[1]
        self.sname = info[2]
        self.layout = info[3]
        self.variant = info[4]
        self.language = info[2]
        self.country = info[3]
        self.extras = info[4]
        self.set_property("margin", 10)

        lab.set_text(self.dname)
        self.pack_start(lab, True, True, 0)
        self.show_all()

class LcLabel(Gtk.Label):
    """ View label for locales, save code duping """
    lc_code = None
    language_name = None

    def __init__(self, lc_code, language_name):
        Gtk.Label.__init__(self)

        self.set_halign(Gtk.Align.START)
        self.lc_code = lc_code
        self.language_name = language_name
        self.set_property("margin", 8)
        self.set_text(self.language_name)
        self.show()

class Components():
    _components = {}
    
    def __init__(self):
        self._components["general_grid"] = Gtk.Grid()
        self._components["scroll_language_win"] = Gtk.ScrolledWindow(None, None)
        self._components["scroll_keyboard_win"] = Gtk.ScrolledWindow(None, None)
        self._components["listbox_language_win"] = Gtk.ListBox()
        self._components["listbox_keyboard_win"] = Gtk.ListBox()
        self._components["more_button_language_win"] = Gtk.Image.new_from_icon_name("view-more-symbolic",
                                                        Gtk.IconSize.MENU)
        self._components["more_button_keyboard_win"] = Gtk.Image.new_from_icon_name("view-more-symbolic",
                                                        Gtk.IconSize.MENU)
        self._components["label_language_win"] = Gtk.Label()
        self._components["label_keyboard_win"] = Gtk.Label()
        self._components["grid_keyboard_win"] = Gtk.Grid()
        self._components["input_keyboard_win"] = Gtk.Entry()

    def get_component(self, component_name):
        return self._components[component_name]

class language_live_page_gtk(BasePageGtk):
    """ Basic language page. """
    _components = None

    had_init = False
    xkb = None
    shown_layouts = None
    extras = None
    nb_default_languages = 2

    def __init__(self, language_manager, config_general):
        BasePageGtk.__init__(self)
       
        self._language_manager = language_manager
        self._config_general = config_general
        self._config_general["language_live_page"] = {}
        self._config_general["language_live_page"]["locale"] = default_locales[2]

        self._config_general["language_live_page"]["language_next"] = False
        self._config_general["language_live_page"]["keyboard_next"] = False
        self._win_parent = None

        self._components = Components()
        self.init_components()
        self.refresh_ui_language()

    def init_components(self):
        # general grid
        self.pack_start(self._components.get_component("general_grid"), True, True, 0)
        self._components.get_component("general_grid").set_margin_start(10)
        self._components.get_component("general_grid").set_margin_end(10)
        self._components.get_component("general_grid").set_margin_top(10)
        self._components.get_component("general_grid").set_margin_bottom(10)
        self._components.get_component("general_grid").set_column_spacing(50)
        self._components.get_component("general_grid").set_row_spacing(5)
        self._components.get_component("general_grid").set_halign(Gtk.Align.START)

        # language box
        self._components.get_component("scroll_language_win").set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self._components.get_component("scroll_language_win").add(self._components.get_component("listbox_language_win"))

        self._components.get_component("scroll_language_win").set_halign(Gtk.Align.CENTER)
        self._components.get_component("listbox_language_win").set_size_request(60, -1)

        self._components.get_component("scroll_language_win").set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        self._components.get_component("more_button_language_win").set_property("margin", 8)
        self._components.get_component("more_button_language_win").show_all()
        self._components.get_component("listbox_language_win").connect_after("row-selected", self.on_row_select_language)

        # title for box
        self._components.get_component("label_language_win").set_halign(Gtk.Align.START)
        self._components.get_component("label_language_win").set_line_wrap(True)

        self._components.get_component("label_keyboard_win").set_halign(Gtk.Align.START)
        self._components.get_component("label_keyboard_win").set_line_wrap(True)

        # keyboard box
        self._components.get_component("grid_keyboard_win").set_row_spacing(6)
        self._components.get_component("grid_keyboard_win").set_halign(Gtk.Align.CENTER)

        self._components.get_component("listbox_keyboard_win").set_size_request(60, -1)

        self._components.get_component("scroll_keyboard_win").set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self._components.get_component("scroll_keyboard_win").add(self._components.get_component("listbox_keyboard_win"))
        self._components.get_component("scroll_keyboard_win").set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self._components.get_component("scroll_keyboard_win").set_vexpand(True)
        self._components.get_component("grid_keyboard_win").attach(self._components.get_component("scroll_keyboard_win"), 0, 0, 2, 1)

        # Input tester
        self._components.get_component("grid_keyboard_win").attach(self._components.get_component("input_keyboard_win"), 0, 1, 2, 1)
        self._components.get_component("more_button_keyboard_win").set_property("margin", 8)
        self._components.get_component("listbox_keyboard_win").connect_after("row-selected", self.on_row_select_keyboard)

        # attach general grid
        self._components.get_component("general_grid").attach(self._components.get_component("scroll_language_win"), 0, 1, 1, 1)
        self._components.get_component("general_grid").attach(self._components.get_component("label_language_win"), 0, 0, 1, 1)
        self._components.get_component("general_grid").attach(self._components.get_component("label_keyboard_win"), 1, 0, 1, 1)
        self._components.get_component("general_grid").attach(self._components.get_component("grid_keyboard_win"), 1, 1, 1, 1)

    def on_row_select_language(self, lbox, newrb=None):
        """ Handle selections of locales """
        self._config_general["language_live_page"]["locale"] = None
        self._config_general["language_live_page"]["locale_sz"] = None
        if not newrb:
            self._config_general["language_live_page"]["language_next"] = False
            self._win_parent.set_can_next(False)
            return
        child = newrb.get_child()
        if child == self._components.get_component("more_button_language_win"):
            self.init_remaining_language()
            return
        self._config_general["language_live_page"]["locale"] = child.lc_code
        self._config_general["language_live_page"]["locale_sz"] = child.language_name

        self._language_manager.change_language_all_files(self._config_general["language_live_page"]["locale"])
        self._win_parent.load_lang()
        self._config_general["language_live_page"]["language_next"] = True
        if self._config_general["language_live_page"]["language_next"] and self._config_general["language_live_page"]["keyboard_next"]:
            self._win_parent.set_can_next(True)
    
    def on_row_select_keyboard(self, lbox, newrb=None):
        """ Handle selections of locales """
        self._config_general["language_live_page"]["keyboard"] = None
        self._config_general["language_live_page"]["keyboard_sz"] = None
        if not newrb:
            self._config_general["language_live_page"]["keyboard"] = None
            self._config_general["language_live_page"]["keyboard_sz"] = None
            self._config_general["language_live_page"]["keyboard_next"] = False
            self._win_parent.set_can_next(False)
            return
        child = newrb.get_child()
        if child == self._components.get_component("more_button_keyboard_win"):
            self.init_remaining_keyboard()
            return
        self._config_general["language_live_page"]["keyboard"] = child.kb
        self._config_general["language_live_page"]["keyboard_sz"] = child.dname
        try:
            subprocess.check_call("setxkbmap {}".format(child.kb), shell=True)
        except Exception as e:
            print("@ERR@: Couldn\'t set the keyboard layout: {}".format(e))

        self._config_general["language_live_page"]["keyboard_next"] = True
        if self._config_general["language_live_page"]["language_next"] and self._config_general["language_live_page"]["keyboard_next"]:
            self._win_parent.set_can_next(True)
        self._components.get_component("input_keyboard_win").set_text("")

    def load_win(self, win):
        self._win_parent = win

    def do_expensive_init(self):
        """ Do the hard work of actually setting up the view """
        Gdk.threads_enter()
        languages = self._language_manager.get_all_languages()
        languages_keys = list(languages.keys())[0:self.nb_default_languages]
        for key in languages_keys:
            self._components.get_component("listbox_language_win").add(LcLabel(key, self._language_manager.print_in_lang("language_live_page", languages[key])))
        self._components.get_component("listbox_language_win").add(self._components.get_component("more_button_language_win"))
        Gdk.threads_leave()

    def init_remaining_language(self):
        """ Add the rest to the list """
        self._components.get_component("scroll_language_win").set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self._components.get_component("scroll_language_win").set_vexpand(True)
        self._components.get_component("scroll_language_win").set_valign(Gtk.Align.FILL)
        self._components.get_component("more_button_language_win").get_parent().hide()
        appends = list()
        languages = self._language_manager.get_all_languages()
        languages_keys = list(languages.keys())[0:self.nb_default_languages]
        for key in languages.keys():
            if key in languages_keys:
                continue
            appends.append(LcLabel(key, self._language_manager.print_in_lang("language_live_page", languages[key])))

        appends.sort(key=lambda x: x.language_name.lower())
        for item in appends:
            self._components.get_component("listbox_language_win").add(item)


    def init_view_keyboard(self):
        """ Initialise ourself from GNOME XKB """
        if self.had_init:
            return
        self.had_init = True
        self.xkb = GnomeDesktop.XkbInfo()

        items = GnomeDesktop.parse_locale(self._config_general["language_live_page"]["locale"])
        if items[0]:
            lang = items[1]
            country = items[2]
        else:
            # Shouldn't ever happen, but ya never know.
            lang = "en"
            country = "US"

        # if self.info.cached_location:
        #     country = self.info.cached_location.upper()

        l = self._config_general["language_live_page"]["locale"]
        success, type_, id_ = GnomeDesktop.get_input_source_from_locale(l)

        kbset = set()
        kbset.update(self.xkb.get_layouts_for_country(country))
        kbset.update(self.xkb.get_layouts_for_language(lang))

        major_layouts = self.xkb.get_all_layouts()
        for item in major_layouts:
            xkbinf = self.xkb.get_layout_info(item)
            if not xkbinf[0]:
                continue
            if xkbinf[3].lower() == country.lower():
                kbset.add(item)

        layouts = list()
        for x in kbset:
            info = self.xkb.get_layout_info(x)
            if not info[0]:
                continue
            widget = KbLabel(x, info)
            layouts.append(widget)

        c = country.lower()
        native = filter(lambda x: x.country.lower() == c, layouts)

        primary = None

        if not native:
            native = layouts
            for item in native:
                if item.layout[:2].lower() == lang.lower() and not item.extras:
                    primary = item
        else:
            for item in native:
                if not item.extras:
                    primary = item
                    break

        self.added = 0
        self.extras = list()

        def append_inner(layout, item):
            if layout in self.shown_layouts:
                return
            if self.added >= 5:
                self.extras.append(item)
                return
            self.shown_layouts.add(layout)
            self._components.get_component("listbox_keyboard_win").add(item)
            self.added += 1

        self.shown_layouts = set()
        if primary:
            append_inner(primary.kb, primary)
        for item in native:
            append_inner(item.kb, item)
        for item in layouts:
            append_inner(item.kb, item)

        self._components.get_component("more_button_keyboard_win").show_all()
        kids = self._components.get_component("listbox_keyboard_win").get_children()
        if kids:
            s = self._components.get_component("listbox_keyboard_win").get_children()[0]
            self._components.get_component("listbox_keyboard_win").select_row(s)
        self._components.get_component("listbox_keyboard_win").add(self._components.get_component("more_button_keyboard_win"))



    def init_remaining_keyboard(self):
        layouts = self.xkb.get_all_layouts()
        self._components.get_component("more_button_keyboard_win").get_parent().hide()

        appends = list()
        # Deal with extras first
        self.extras = sorted(self.extras, key=lambda x: x.dname)
        for item in self.extras:
            if item.kb in self.shown_layouts:
                continue
            self.shown_layouts.add(item.kb)
            self._components.get_component("listbox_keyboard_win").add(item)

        for layout in layouts:
            # Don't dupe
            if layout in self.shown_layouts:
                continue
            info = self.xkb.get_layout_info(layout)
            success = info[0]
            if not success:
                continue

            widget = KbLabel(layout, info)
            appends.append(widget)
        appends.sort(key=lambda x: x.dname.lower())
        for app in appends:
            if app.kb in self.shown_layouts:
                continue
            self._components.get_component("listbox_keyboard_win").add(app)

    def prepare(self):
        # Nothing to seed with.
        self.init_view_keyboard()
        if "locale" in self._config_general["language_live_page"] and "keyboard" in self._config_general["language_live_page"]:
            self._win_parent.set_can_next(True)
        else:
            self._win_parent.set_can_next(False)


    def refresh_ui_language(self):
        self._components.get_component("label_language_win").set_markup(u"<span font-size='medium'>{}</span>".format(self._language_manager.print_in_lang("language_live_page", "desc_language")))
        self._components.get_component("label_keyboard_win").set_markup(u"<span font-size='medium'>{}</span>".format(self._language_manager.print_in_lang("language_live_page", "desc_keyboard")))
        self._components.get_component("input_keyboard_win").set_placeholder_text(self._language_manager.print_in_lang("language_live_page", "input_keyboard"))
        
        if self._components.get_component("more_button_language_win").is_visible():
           pass
        else:
            for label in self._components.get_component("listbox_language_win").get_children():
                self._components.get_component("listbox_language_win").remove(label)
            languages = self._language_manager.get_all_languages()
            languages_keys = list(languages.keys())[0:self.nb_default_languages]
            for key in languages_keys:
                self._components.get_component("listbox_language_win").add(LcLabel(key, self._language_manager.print_in_lang("language_live_page", languages[key])))
            self._components.get_component("listbox_language_win").add(self._components.get_component("more_button_language_win"))
    #title
    def get_title(self):
        return self._language_manager.print_in_lang("language_live_page", "title")

    #sidebar
    def get_sidebar_title(self):
        return self._language_manager.print_in_lang("language_live_page", "sidebar_title")

    #id
    def get_name(self):
        return "language_live"
   
    #icon
    def get_icon_name(self, plasma=False):
        return "preferences-desktop-locale"