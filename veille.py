#!/usr/bin/env python3
"""Affiche veille.html en plein écran sur chaque moniteur (GTK + WebKit),
et se ferme à la première touche, clic, défilement ou mouvement de souris."""
import glob
import os
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('WebKit2', '4.1')
from gi.repository import Gtk, Gdk, GLib, WebKit2

PAGE = 'file://' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'veille.html')
SEUIL_SOURIS = 12  # pixels avant de considérer que la souris a vraiment bougé

origine = {}
vues = []


def lire_batterie():
    """Renvoie (pourcentage, en_charge) ou None s'il n'y a pas de batterie."""
    for bat in sorted(glob.glob('/sys/class/power_supply/BAT*')):
        try:
            with open(os.path.join(bat, 'capacity')) as f:
                niveau = int(f.read().strip())
            with open(os.path.join(bat, 'status')) as f:
                statut = f.read().strip()
            return niveau, statut in ('Charging', 'Full')
        except (OSError, ValueError):
            continue
    return None


def envoyer_batterie(*_):
    bat = lire_batterie()
    if bat:
        js = f'typeof setBatterie === "function" && setBatterie({bat[0]}, {str(bat[1]).lower()})'
        for view in vues:
            view.evaluate_javascript(js, -1, None, None, None, None, None)
    return True


def page_chargee(_view, event):
    if event == WebKit2.LoadEvent.FINISHED:
        envoyer_batterie()


def quitter(*_):
    Gtk.main_quit()
    return True


def mouvement(_widget, event):
    pos = (event.x_root, event.y_root)
    if 'p' not in origine:
        origine['p'] = pos
    elif abs(pos[0] - origine['p'][0]) + abs(pos[1] - origine['p'][1]) > SEUIL_SOURIS:
        quitter()
    return True


def ouvrir_fenetre(display, n):
    win = Gtk.Window()
    win.set_title('Veille Monde Sombre')

    view = WebKit2.WebView()
    view.get_settings().set_enable_developer_extras(False)
    view.set_background_color(Gdk.RGBA(0, 0, 0, 1))
    view.connect('load-changed', page_chargee)
    view.load_uri(PAGE)
    vues.append(view)
    for signal in ('key-press-event', 'button-press-event', 'scroll-event'):
        view.connect(signal, quitter)
    view.connect('motion-notify-event', mouvement)

    win.add(view)
    win.connect('destroy', quitter)
    win.show_all()
    win.fullscreen_on_monitor(win.get_screen(), n)
    win.get_window().set_cursor(Gdk.Cursor.new_for_display(display, Gdk.CursorType.BLANK_CURSOR))


def main():
    display = Gdk.Display.get_default()
    for n in range(display.get_n_monitors()):
        ouvrir_fenetre(display, n)
    GLib.timeout_add_seconds(20, envoyer_batterie)
    Gtk.main()


if __name__ == '__main__':
    main()
