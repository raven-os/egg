from gi.repository import Gtk, Gdk, GObject, GnomeDesktop
from ui.gtk.main_window_button import MainWindowButton
from ui.gtk.pages.page import Page
import subprocess
import locale


class KeyboardLabel(Gtk.Label):
    keyboard_name = None
    keyboard_id = None

    def __init__(self, keyboard_id: str, keyboard_name: str) -> None:
        Gtk.Label.__init__(self)
        self.keyboard_id = keyboard_id
        self.keyboard_name = keyboard_name

        self.set_property('margin', 10)
        self.set_halign(Gtk.Align.START)
        self.set_text(self.keyboard_name)
        self.show()


class LanguageLabel(Gtk.Label):
    language_code = None
    language_name = None

    def __init__(self, language_code: str, language_name: str) -> None:
        Gtk.Label.__init__(self)
        self.language_code = language_code
        self.language_name = language_name

        self.set_property('margin', 8)
        self.set_halign(Gtk.Align.START)
        self.set_text(self.language_name)
        self.show()


class Components():
    _components = {}

    def __init__(self) -> None:
        self._components['general_box'] = Gtk.Box(self, orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self._components['general_grid'] = Gtk.Grid()
        self._components['language_window_scroll'] = Gtk.ScrolledWindow(None, None)
        self._components['keyboard_window_scroll'] = Gtk.ScrolledWindow(None, None)
        self._components['language_window_listbox'] = Gtk.ListBox()
        self._components['keyboard_window_listbox'] = Gtk.ListBox()
        self._components['language_window_more_btn'] = Gtk.Image.new_from_icon_name('view-more-symbolic',
                                                                                    Gtk.IconSize.MENU)
        self._components['keyboard_window_more_btn'] = Gtk.Image.new_from_icon_name('view-more-symbolic',
                                                                                    Gtk.IconSize.MENU)
        self._components['language_window_label'] = Gtk.Label()
        self._components['keyboard_window_label'] = Gtk.Label()
        self._components['keyboard_window_grid'] = Gtk.Grid()
        self._components['keyboard_window_input'] = Gtk.Entry()

    def get_component(self, component_name: str) -> GObject:
        return self._components[component_name]


class LanguageLivePage(Page):
    _components = None
    _win_parent = None

    keyboard_already_showed = set()
    country_depending_keyboard = list()
    nb_default_languages = 2
    nb_default_keyboard = 7

    def __init__(self, locale_general: dict, config_general: dict) -> None:
        super(LanguageLivePage, self).__init__()
        self._locale_general = locale_general
        self._config_general = config_general
        self._config_general['language_live_page'] = {}
        self._config_general['language_live_page']['locale'] = self._locale_general.current_language
        self._config_general['language_live_page']['language_next'] = False
        self._config_general['language_live_page']['keyboard_next'] = False

        self._components = Components()
        self.init_components()
        self.refresh_ui_language()

    def init_components(self) -> None:
        # General grid
        self._components.get_component('general_box').pack_start(self._components.get_component('general_grid'), True,
                                                                 True, 0)
        self._components.get_component('general_grid').set_margin_start(10)
        self._components.get_component('general_grid').set_margin_end(10)
        self._components.get_component('general_grid').set_margin_top(10)
        self._components.get_component('general_grid').set_margin_bottom(10)
        self._components.get_component('general_grid').set_column_spacing(50)
        self._components.get_component('general_grid').set_row_spacing(5)
        self._components.get_component('general_grid').set_halign(Gtk.Align.START)

        # Language box
        self._components.get_component('language_window_scroll').set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self._components.get_component('language_window_scroll').add(
            self._components.get_component('language_window_listbox'))

        self._components.get_component('language_window_scroll').set_halign(Gtk.Align.CENTER)
        self._components.get_component('language_window_listbox').set_size_request(60, -1)

        self._components.get_component('language_window_scroll').set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        self._components.get_component('language_window_more_btn').set_property('margin', 8)
        self._components.get_component('language_window_more_btn').show_all()
        self._components.get_component('language_window_listbox').connect_after('row-selected', self.on_row_click_language)

        # Title for box
        self._components.get_component('language_window_label').set_halign(Gtk.Align.START)
        self._components.get_component('language_window_label').set_line_wrap(True)

        self._components.get_component('keyboard_window_label').set_halign(Gtk.Align.START)
        self._components.get_component('keyboard_window_label').set_line_wrap(True)

        # Keyboard box
        self._components.get_component('keyboard_window_grid').set_row_spacing(6)
        self._components.get_component('keyboard_window_grid').set_halign(Gtk.Align.CENTER)

        self._components.get_component('keyboard_window_listbox').set_size_request(60, -1)

        self._components.get_component('keyboard_window_scroll').set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self._components.get_component('keyboard_window_scroll').add(
            self._components.get_component('keyboard_window_listbox'))
        self._components.get_component('keyboard_window_scroll').set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self._components.get_component('keyboard_window_scroll').set_vexpand(True)
        self._components.get_component('keyboard_window_grid').attach(
            self._components.get_component('keyboard_window_scroll'), 0, 0, 2, 1)

        # Input tester
        self._components.get_component('keyboard_window_grid').attach(self._components.get_component('keyboard_window_input'),
                                                                   0, 1, 2, 1)
        self._components.get_component('keyboard_window_more_btn').set_property('margin', 8)
        self._components.get_component('keyboard_window_listbox').connect_after('row-selected', self.on_row_click_keyboard)

        # Attach general grid
        self._components.get_component('general_grid').attach(self._components.get_component('language_window_scroll'), 0,
                                                              1, 1, 1)
        self._components.get_component('general_grid').attach(self._components.get_component('language_window_label'), 0,
                                                              0, 1, 1)
        self._components.get_component('general_grid').attach(self._components.get_component('keyboard_window_label'), 1,
                                                              0, 1, 1)
        self._components.get_component('general_grid').attach(self._components.get_component('keyboard_window_grid'), 1, 1,
                                                              1, 1)

    def on_row_click_language(self, list_box_language, current_row_language_clicked=None) -> None:
        if not current_row_language_clicked:
            self._config_general['language_live_page']['locale'] = None
            self._config_general['language_live_page']['locale_sz'] = None
            self._config_general['language_live_page']['language_next'] = False
            self._win_parent.set_button_action_visibility(MainWindowButton.NEXT, False)
            return

        row_elem = current_row_language_clicked.get_child()
        if row_elem != self._components.get_component('language_window_more_btn'):
            self._config_general['language_live_page']['locale'] = row_elem.language_code
            self._config_general['language_live_page']['locale_sz'] = row_elem.language_name

            self._locale_general.change_language_all_files(self._config_general['language_live_page']['locale'])
            self._win_parent.load_lang()
            self._config_general['language_live_page']['language_next'] = True
            if self._config_general['language_live_page']['language_next'] and \
                    self._config_general['language_live_page']['keyboard_next']:
                self._win_parent.set_button_action_visibility(MainWindowButton.NEXT, True)
            return

        self._components.get_component('language_window_scroll').set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self._components.get_component('language_window_scroll').set_vexpand(True)
        self._components.get_component('language_window_scroll').set_valign(Gtk.Align.FILL)
        self._components.get_component('language_window_more_btn').get_parent().hide()
        languages = self._locale_general.available_languages
        languages_keys = list(languages)[0:self.nb_default_languages]
        languages_extra = list()
        for key in languages:
            if key in languages_keys:
                continue
            languages_extra.append(
                LanguageLabel(key, self._locale_general.translate_msg('language_live_page', languages[key])))

        languages_extra.sort(key=lambda sort: sort.language_name.lower())
        for current in languages_extra:
            self._components.get_component('language_window_listbox').add(current)
        self.set_selected_language_row()

    def on_row_click_keyboard(self, list_box_keyboard, current_row_keyboard_clicked=None) -> None:
        if not current_row_keyboard_clicked:
            self._config_general['language_live_page']['keyboard'] = None
            self._config_general['language_live_page']['keyboard_sz'] = None
            self._config_general['language_live_page']['keyboard_next'] = False
            self._win_parent.set_button_action_visibility(MainWindowButton.NEXT, False)
            return

        row_elem = current_row_keyboard_clicked.get_child()
        if row_elem != self._components.get_component('keyboard_window_more_btn'):
            self._config_general['language_live_page']['keyboard'] = row_elem.keyboard_id
            self._config_general['language_live_page']['keyboard_sz'] = row_elem.keyboard_name
            self.set_keyboard()
            self._config_general['language_live_page']['keyboard_next'] = True
            if self._config_general['language_live_page']['language_next'] and \
                    self._config_general['language_live_page']['keyboard_next']:
                self._win_parent.set_button_action_visibility(MainWindowButton.NEXT, True)
            self._components.get_component('keyboard_window_input').set_text('')
            return

        self._components.get_component('keyboard_window_more_btn').get_parent().hide()

        keyboard_info = GnomeDesktop.XkbInfo()
        all_keyboard_code_info = keyboard_info.get_all_layouts()
        all_expand_languages = list()

        for current in self.country_depending_keyboard:
            if not current.keyboard_id in self.keyboard_already_showed:
                self.keyboard_already_showed.add(current.keyboard_id)
                all_expand_languages.append(current)

        for current in all_keyboard_code_info:
            if not current in self.keyboard_already_showed:
                info = keyboard_info.get_layout_info(current)
                if info[0]:
                    all_expand_languages.append(KeyboardLabel(current, info.display_name))

        all_expand_languages.sort(key=lambda sort: sort.keyboard_name.lower())
        for current in all_expand_languages:
            if not current.keyboard_id in self.keyboard_already_showed:
                self._components.get_component('keyboard_window_listbox').add(current)
        self.set_selected_keyboard_row()

    def init_view_keyboard(self) -> None:
        keyboard_info = GnomeDesktop.XkbInfo()
        country = self._locale_general.get_detailed_locale_country(
            self._config_general['language_live_page']['locale'])
        country_lower = country.lower()
        input_locale = GnomeDesktop.get_input_source_from_locale(
            self._locale_general.get_detailed_locale(self._config_general['language_live_page']['locale']))

        keyboard_depending_language = list([input_locale.id])
        keyboard_depending_language_after = list()
        all_keyboard_and_extra = list()

        all_keyboard = keyboard_info.get_all_layouts()
        for current in all_keyboard:
            info = keyboard_info.get_layout_info(current)
            if not info[0]:
                continue
            if info[3].lower() == country_lower:
                keyboard_depending_language_after.append(current)

        keyboard_depending_language_after.remove(input_locale.id)
        keyboard_depending_language_after = sorted(keyboard_depending_language_after)
        keyboard_depending_language.extend(keyboard_depending_language_after)

        for current in keyboard_depending_language:
            info = keyboard_info.get_layout_info(current)
            if info[0]:
                all_keyboard_and_extra.append(KeyboardLabel(current, info.display_name))

        for current in all_keyboard_and_extra:
            if current.keyboard_id in self.keyboard_already_showed:
                continue
            if len(self.keyboard_already_showed) >= self.nb_default_keyboard:
                self.country_depending_keyboard.append(current)
                continue
            self.keyboard_already_showed.add(current.keyboard_id)
            self._components.get_component('keyboard_window_listbox').add(current)

        self._components.get_component('keyboard_window_more_btn').show_all()
        self._components.get_component('keyboard_window_listbox').add(
            self._components.get_component('keyboard_window_more_btn'))
        self.set_selected_keyboard_row()

    def set_keyboard(self) -> None:
        if 'keyboard' in self._config_general['language_live_page']\
                and self._config_general['language_live_page']['keyboard'] != None:
            try:
                subprocess.check_call("setxkbmap {}".format(self._config_general['language_live_page']['keyboard']),
                                      shell=True)
            except Exception as e:
                pass

    def set_system_language(self) -> None:
        if 'locale' in self._config_general['language_live_page']\
                and self._config_general['language_live_page']['locale']\
                in self._locale_general.available_languages:
            locale_detailed = self._locale_general.get_detailed_locale(
                self._config_general['language_live_page']['locale'])
            locale.setlocale(locale.LC_ALL, locale_detailed)

    def set_selected_language_row(self) -> None:
        check_not_empty = self._components.get_component('language_window_listbox').get_children()
        if not check_not_empty:
            return

        for current in self._components.get_component('language_window_listbox').get_children():
            label = current.get_child()
            if label != self._components.get_component('language_window_more_btn')\
                    and 'locale' in self._config_general['language_live_page']\
                    and label.language_code == self._config_general['language_live_page']['locale']:
                self._components.get_component('language_window_listbox').select_row(current)
                return

    def set_selected_keyboard_row(self) -> None:
        check_not_empty = self._components.get_component('keyboard_window_listbox').get_children()
        if not check_not_empty:
            return
        selected_row = self._components.get_component('keyboard_window_listbox').get_children()[0]
        self._components.get_component('keyboard_window_listbox').select_row(selected_row)

    def long_task(self):
        Gdk.threads_enter()
        languages = self._locale_general.available_languages
        languages_keys = list(languages)[0:self.nb_default_languages]
        languages_label = list()
        for key in languages_keys:
            languages_label.append(
                LanguageLabel(key, self._locale_general.translate_msg('language_live_page', languages[key])))

        languages_label.sort(key=lambda sort: sort.language_name.lower())
        for current in languages_label:
            self._components.get_component('language_window_listbox').add(current)

        self._components.get_component('language_window_listbox').add(
            self._components.get_component('language_window_more_btn'))
        self.set_selected_language_row()
        self.init_view_keyboard()
        Gdk.threads_leave()

    def load_win(self, win) -> None:
        self._win_parent = win

    def load_page(self) -> None:
        self.set_system_language()
        self.set_keyboard()
        self.set_selected_language_row()
        self.set_selected_keyboard_row()

        self._win_parent.set_button_action_visibility(MainWindowButton.NEXT, 'locale' in self._config_general['language_live_page']\
            and 'keyboard' in self._config_general['language_live_page'])

    def refresh_ui_language(self) -> None:
        self._components.get_component('language_window_label').set_markup(u'<span font-size="medium">{}</span>'.format(
            self._locale_general.translate_msg('language_live_page', 'desc_language')))
        self._components.get_component('keyboard_window_label').set_markup(u'<span font-size="medium">{}</span>'.format(
            self._locale_general.translate_msg('language_live_page', 'desc_keyboard')))
        self._components.get_component('keyboard_window_input').set_placeholder_text(
            self._locale_general.translate_msg('language_live_page', 'input_keyboard'))

        self.set_system_language()

        languages = self._locale_general.available_languages
        keyboard_info = GnomeDesktop.XkbInfo()

        for current_row in self._components.get_component('language_window_listbox').get_children():
            label = current_row.get_child()
            if label != self._components.get_component('language_window_more_btn'):
                label.language_name = self._locale_general.translate_msg('language_live_page',
                                                                           languages[label.language_code])
                label.set_text(label.language_name)

        for current_row in self._components.get_component('keyboard_window_listbox').get_children():
            label = current_row.get_child()
            if label != self._components.get_component('keyboard_window_more_btn'):
                info = keyboard_info.get_layout_info(label.keyboard_id)
                label.keyboard_name = info.display_name
                label.set_text(label.keyboard_name)

    def get_page_title(self) -> str:
        return self._locale_general.translate_msg('language_live_page', 'title')

    def get_page_sidebar_title(self) -> str:
        return self._locale_general.translate_msg('language_live_page', 'sidebar_title')

    def get_page_id(self) -> str:
        return self._config_general['config_page']['language_live']['id']

    def get_page_icon(self) -> str:
        return self._config_general['config_page']['language_live']['icon']
