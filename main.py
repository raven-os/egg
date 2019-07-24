#!/usr/bin/env python3.7
import containers
import events
import json
import sys
import os


def load_lang_files(locale_general, config_general):
    locale_general.set_locales_folder(config_general["locales_folder"])
    locale_general.change_language_all_files(config_general["default_language_code"])
    for current_language_file in config_general["language_files"]:
        locale_general.change_language_file(locale_general.get_current_language(), current_language_file)


def load_config_from_files(config_files):
    config_files_path = {}
    prefix_path = "./"
    prefix_path_dev = os.getcwd() + "/"
    suffix_dev = "_dev"

    for item in config_files:
        if __debug__:
            file_path = prefix_path_dev + "config/" + item + suffix_dev + ".json"
            if not os.path.isfile(file_path):
                file_path = prefix_path + "config/" + item + ".json"
        else:
            file_path = prefix_path + "config/" + item + ".json"
        config_files_path[item] = file_path

    return config_files_path


def load_config_files():
    config_files = {}

    config_files["general"] = "general"
    config_files["main_window"] = "main_window"
    config_files_path = load_config_from_files(config_files)

    with open(config_files_path["general"], 'r') as datafile:
        config = json.load(datafile)
        containers.Configs.config.override(config)

    with open(config_files_path["main_window"], 'r') as datafile:
        config = json.load(datafile)
        containers.Configs.config_main_window_page.override(config)


def main():
    load_config_files()

    config_general = containers.Configs.config()
    load_lang_files(containers.Locales.locale_general(), config_general)

    if not config_general["launch_without_root"]:
        if os.geteuid() != 0:
            containers.GraphicGui.custom_modal_gtk().launch(
                containers.Locales.locale_general().print_in_lang("custom_modal", "not_admin_title_modal"),
                containers.Locales.locale_general().print_in_lang("custom_modal", "not_admin_desc_modal"),
                events.type_event.TypeEvent.INFO)
            sys.exit(1)

    app = containers.GraphicGui.welcome_window_gtk()
    app.launch()


if __name__ == '__main__':
    main()
