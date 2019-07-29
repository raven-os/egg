#!/usr/bin/env python3
import json
import os
import sys

from egg.app import App
from egg.containers import Configs, Locales
from egg.type_event import TypeEvent

gtk_found = False

try:
    from ui.gtk.app import GtkApp
    gtk_found = True
except (ValueError, ImportError):
    pass


def load_lang_files(locale_general, config_general):
    locale_general.locales_folder = config_general['locales_folder']
    locale_general.change_language_all_files(config_general['default_language_code'])
    for current_language_file in config_general['language_files']:
        locale_general.change_language_file(locale_general.current_language, current_language_file)


def load_config_from_files(config_files):
    config_files_path = {}
    prefix_path = './'
    prefix_path_dev = os.getcwd() + '/'
    suffix_dev = '_dev'

    for item in config_files:
        if __debug__:
            file_path = prefix_path_dev + 'config/' + item + suffix_dev + '.json'
            if not os.path.isfile(file_path):
                file_path = prefix_path + 'config/' + item + '.json'
        else:
            file_path = prefix_path + 'config/' + item + '.json'
        config_files_path[item] = file_path

    return config_files_path


def load_config_files():
    config_files = {'general': 'general', 'main_window': 'main_window'}

    config_files_path = load_config_from_files(config_files)

    with open(config_files_path['general'], 'r') as datafile:
        config = json.load(datafile)
        Configs.general.override(config)

    with open(config_files_path['main_window'], 'r') as datafile:
        config = json.load(datafile)
        Configs.main_window.override(config)


def main():
    load_config_files()

    config_general = Configs.general()
    load_lang_files(Locales.locale_general(), config_general)

    ui_app = App()
    if gtk_found:
        ui_app = GtkApp()

    if not config_general['launch_without_root']:
        if os.geteuid() != 0:
            ui_app.display_popup(Locales.locale_general().translate_msg('popup', 'not_admin_title_popup'),
                                 Locales.locale_general().translate_msg('popup', 'not_admin_desc_popup'),
                                 TypeEvent.INFO)
            sys.exit(1)
    ui_app.launch()


if __name__ == '__main__':
    main()
