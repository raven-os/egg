import eggroot.containers
import sys
import os
# print("win1 gtk.py's __name__: {}".format(__name__))
# print("win1 gtk.py's __package__: {}".format(__package__))
# pass text for config all by text

def load_lang_files(locale_general):
    # put all the file and the language in the config containers
    locale_general.change_language_file(locale_general.get_current_language(), 'welcome_win')
    locale_general.change_language_file(locale_general.get_current_language(), 'custom_modal')

def main():
    # configuration and choose GUI type
    gtk = True
    eggroot.containers.Configs.config.override({
        "os-name": "Raven-OS",
        "nom": "dupont",
        "prenom": "jean-louis"
    })


    # init lang file
    load_lang_files(eggroot.containers.Locales.locale_general())

    if gtk == True:
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
        if os.geteuid() != 0:
            sys.stderr.write("You must be root to use OsInstaller\n")
            sys.stderr.flush()
            sys.exit(1)
        app = eggroot.containers.GraphicGui.welcome_win_ncurses()
    app.lunch()

if __name__ == '__main__':
    main()