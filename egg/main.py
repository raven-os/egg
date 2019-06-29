import eggroot.gtk.win1_gtk
import eggroot.ncurses.win1_ncurses
import eggroot.containers

# print("win1 gtk.py's __name__: {}".format(__name__))
# print("win1 gtk.py's __package__: {}".format(__package__))
# pass text for config all by text

def main():
    gtk = True

    eggroot.containers.Configs.config.override({
        "nom": "dupont",
        "prenom": "jean-louis"
    })

    if gtk == True:
        w = eggroot.containers.Clients.win_gtk()
    elif gtk == False:
        w = eggroot.containers.Clients.win_ncurses()
    w.lunch()

if __name__ == '__main__':
    main()