from coregame import coregame as coregame

import uielements.text as text
import uielements.surface as surface
import uielements.button as button
import uielements.checkbox as checkbox

import userstatistics

import sys
import os


# Permet de récupérer le chemmin complet aux images
def resource_path(relative_path):
    # SI sys._MEIPASS existe, c'est que le jeu a été lancé depuis le .exe
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def centretexte(textsize, espace):  # Utilitaire pour center un texte ! Retourne la position x et y du texte
    return int(espace[0] / 2 - textsize[0] / 2), int(espace[1] / 2 - textsize[1] / 2)


def checkmousebouton(mousepos, buttonx, buttony, buttonwidth,
                     buttonheight):  # Utilitaire pour savoir si la souris se trouve dedans un bouton
    posx, posy = mousepos[0], mousepos[1]
    minx, maxx = buttonx, buttonx + buttonwidth
    miny, maxy = buttony, buttony + buttonheight
    if posx >= minx and posx <= maxx and posy >= miny and posy <= maxy:
        return True
    return False


def getrunner():  # retourne le personnage avec lequel le joueur va jouer à partir de ses stats (gros, normal ou athlète)
    stats_obj = userstatistics.UserStatistics.stats
    if stats_obj.nb_courses - stats_obj.nb_courses_echouees >= 100 and stats_obj.score_total >= 250000 and stats_obj.haies_traversees >= 300 and stats_obj.total_dist >= 42195:
        # Au moins 100 courses gagnés, un score total d'au moins 250000, avoir traversé au moins 300 haies, avoir une distance totale d'au moins 42,195 km (marathon :p)
        return "athlete"
    if stats_obj.nb_courses - stats_obj.nb_courses_echouees >= 10 and stats_obj.score_total >= 20000 and stats_obj.haies_traversees >= 50:
        # Au moins 10 courses gagnés, un score total d'au moins 20000, avoir traversé au moins 50 haies
        return "normal"
    return "gros"


def computetime(num_value):
    temps_ms = coregame.CoreGame.current_core.time

    if num_value:
        return temps_ms

    aff_ms = str(temps_ms % 1000)
    temps_s = int(temps_ms // 1000)
    aff_s = temps_s % 60
    temps_min = int(temps_s // 60)

    if aff_s < 10:
        aff_s = "0" + str(aff_s)
    else:
        aff_s = str(aff_s)

    return str(temps_min) + ":" + aff_s + "." + aff_ms


def computedistance(num_value):
    distance = coregame.CoreGame.current_core.distance

    if num_value:
        return distance

    return "%.0f" % round(distance, 0) + " m"


def delete_menu_obj():
    for bouton in list(button.Button.getButtons()):
        bouton.unreferance()
    for surf in list(surface.Surface.getSurfaces()):
        surf.unreferance()
    for txt in list(text.Text.getTexts()):
        txt.unreferance()
    for check in list(checkbox.Checkbox.getCheckboxes()):
        check.unreferance()


def isvalidint(supposedint):
    var = True if (supposedint is not None and int(supposedint) is not None) else False
    return var
