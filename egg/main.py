import eggroot.containers
import json
import sys
import os
# print("win1 gtk.py's __name__: {}".format(__name__))
# print("win1 gtk.py's __package__: {}".format(__package__))
# pass text for config all by text

def load_lang_files(locale_general, config_general):
    locale_general.set_locales_folder(config_general["locales_folder"])
    locale_general.change_language_all_files(config_general["default_language_code"])
    for current_language_file in config_general["language_files"]:
        locale_general.change_language_file(locale_general.get_current_language(), current_language_file)

def load_config_files():
    if __debug__:
        prefix_path = "/home/desaye_c/tek/egg/egg/"
        prefix_dev = "_dev"
    else:
        prefix_path = "./"
        prefix_dev = ""

    general_config_file = prefix_path + "config/general" + prefix_dev + ".json"
    with open(general_config_file, 'r') as datafile:
        config = json.load(datafile)
        eggroot.containers.Configs.config.override(config)

    main_window_config_file =  prefix_path + "config/main_window" + prefix_dev + ".json"
    with open(main_window_config_file, 'r') as datafile:
        config = json.load(datafile)
        eggroot.containers.Configs.config_main_window_page.override(config)

def main():
    # configuration and choose GUI type
    gtk = True
  
    # init all config files
    load_config_files()
    # init lang file
    config_general = eggroot.containers.Configs.config()
    load_lang_files(eggroot.containers.Locales.locale_general(), config_general)

    # check cette histoire de permissions
    # # Immediately drop permissions before we init GTK
    # p = PermissionsManager()
    # p.down_permissions()


    if gtk == True:
        if not config_general["lunch_without_root"]:
            if os.geteuid() != 0:
                eggroot.containers.GraphicGui.custom_modal_gtk().lunch(
                eggroot.containers.Locales.locale_general().print_in_lang("custom_modal", "not_admin_title_modal"),
                eggroot.containers.Locales.locale_general().print_in_lang("custom_modal", "not_admin_desc_modal",),
                eggroot.general.type_event.type_event.INFO)
                sys.exit(1)
        # initialisation des threads GTK
        # GObject.threads_init()
        # Gdk.threads_init()
        app = eggroot.containers.GraphicGui.welcome_win_gtk()
    else:
        if not config_general["lunch_without_root"]:
            if os.geteuid() != 0:
                sys.stderr.write("You must be root to use OsInstaller\n")
                sys.stderr.flush()
                sys.exit(1)
            app = eggroot.containers.GraphicGui.welcome_win_ncurses()
    app.lunch()

if __name__ == '__main__':
    main()