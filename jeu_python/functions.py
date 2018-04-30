from coregame import coregame as coregame

import uielements.text as text
import uielements.surface as surface
import uielements.button as button
import uielements.checkbox as checkbox
import uielements.tab as tab
import uielements.textbox as textbox

import constantes
import userstatistics
import view
import pycurl
import onlineconnector

import json
import sys
import os
import hashlib


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


def computetime(num_value, customtime=None):
    temps_ms = customtime or coregame.CoreGame.current_core.time

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


def computeplaytime(temps_ms):
    temps_s = temps_ms / 1000
    aff_s = str(int(temps_s % 60)) + " s "
    temps_min = temps_s / 60
    aff_m = str(int(temps_min % 60)) + " m "
    temps_h = temps_min / 60
    aff_h = str(int(temps_h % 24)) + " h "
    temps_jour = temps_h / 24
    aff_j = str(int(temps_jour % 365.25)) + " j "

    if temps_jour >= 1:
        return aff_j + aff_h + aff_m + aff_s
    elif temps_h >= 1:
        return aff_h + aff_m + aff_s
    elif temps_min >= 1:
        return aff_m + aff_s
    elif temps_s >= 1:
        return aff_s


def computedistance(num_value, customdistance=None):
    distance = customdistance or coregame.CoreGame.current_core.distance

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
    for tabb in list(tab.Tab.getTabs()):
        tabb.unreferance()
    for textboxe in list(textbox.Textbox.getTextboxes()):
        textboxe.unreferance()


def displaybestscore(stype, level):
    for txt in list(text.Text.getTexts()):
        if txt.absy > 110:  # ATTENTION: MANIERE EXTREMEMENT HACKY DE DETERMINER CE QU'IL FAUT EFFACER !!
            txt.unreferance()

    SCALE_X = 0.3
    SCALE_Y = 0
    LARGEUR = 200
    HAUTEUR = 50
    POSITION_X = -int(LARGEUR / 2)
    POSITION_Y = 130
    SCALE_WIDTH = 0
    SCALE_HEIGHT = 0
    COULEUR = constantes.BLACK
    ANTIALIAS = False
    COULEUR_TEXTE = constantes.BLACK
    FONT = "Arial"
    TAILLE_FONT = 24
    CENTRE_X = False
    CENTRE_Y = True
    ARRIERE_PLAN = None
    ECART = 0
    BORDURE = 0  # rempli
    SEUL = True

    text.Text("Score :", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
              ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
              LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

    stats_obj = userstatistics.UserStatistics.stats
    if stype == "Personnel":
        suffix400 = stats_obj.best_score[level]["400m"] or "N/A"
        suffix400h = stats_obj.best_score[level]["400m haie"] or "N/A"
        suffixci = stats_obj.best_score[level]["Course infinie"] or "N/A"
        if type(suffix400) == float:
            suffix400 = int(suffix400)
        if type(suffix400h) == float:
            suffix400h = int(suffix400h)
        if type(suffixci) == float:
            suffixci = int(suffixci)

        suffix400gm = stats_obj.best_gm_score[level]["400m"] or "N/A"
        suffix400hgm = stats_obj.best_gm_score[level]["400m haie"] or "N/A"
        suffixcigm = stats_obj.best_gm_score[level]["Course infinie"] or "N/A"
        if type(suffix400gm) == int:
            suffix400gm = computetime(False, suffix400gm)
        if type(suffix400hgm) == int:
            suffix400hgm = computetime(False, suffix400hgm)
        if type(suffixcigm) == float or type(suffixcigm) == int:
            suffixcigm = computedistance(False, suffixcigm)
    elif stype == "Global":
        # Convertir le score récuperer de la DB en fichier json valide
        decoded = None
        connection = onlineconnector.OnlineConnector.current_connection
        if connection.data:
            decoded = json.loads(connection.data)

        lvl = str("F" if level == "Facile" else ("M" if level == "Moyen" else "D"))
        suffix400 = suffix400h = suffixci = suffix400gm = suffix400hgm = suffixcigm = "N/A"

        if lvl in decoded:
            if "Q" in decoded[lvl]:
                suffix400 = int(float(decoded[lvl]["Q"]["score"]))
                suffix400gm = computetime(False, float(decoded[lvl]["Q"]["time"]))
            if "QH" in decoded[lvl]:
                suffix400h = int(float(decoded[lvl]["QH"]["score"]))
                suffix400hgm = computetime(False, float(decoded[lvl]["QH"]["time"]))
            if "I" in decoded[lvl]:
                suffixci = int(float(decoded[lvl]["I"]["score"]))
                suffixcigm = computedistance(False, float(decoded[lvl]["I"]["time"]))

    SCALE_X = 0.3
    SCALE_Y = 0
    LARGEUR = 200
    HAUTEUR = 50
    POSITION_X = -int(LARGEUR / 2)
    POSITION_Y = 185
    SCALE_WIDTH = 0
    SCALE_HEIGHT = 0
    COULEUR = constantes.BLACK
    ANTIALIAS = False
    COULEUR_TEXTE = constantes.BLACK
    FONT = "Arial"
    TAILLE_FONT = 20
    CENTRE_X = False
    CENTRE_Y = True
    ARRIERE_PLAN = None
    ECART = 0
    BORDURE = 0  # rempli
    SEUL = True

    text.Text("400m: " + str(suffix400), ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
              ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
              LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

    POSITION_Y += 55

    text.Text("400m haie: " + str(suffix400h), ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
              ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
              LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

    POSITION_Y += 55

    text.Text("Course infinie: " + str(suffixci), ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
              ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
              LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

    SCALE_X = 0.7
    SCALE_Y = 0
    LARGEUR = 200
    HAUTEUR = 50
    POSITION_X = -int(LARGEUR / 2)
    POSITION_Y = 130
    SCALE_WIDTH = 0
    SCALE_HEIGHT = 0
    COULEUR = constantes.BLACK
    ANTIALIAS = False
    COULEUR_TEXTE = constantes.BLACK
    FONT = "Arial"
    TAILLE_FONT = 24
    CENTRE_X = False
    CENTRE_Y = True
    ARRIERE_PLAN = None
    ECART = 0
    BORDURE = 0  # rempli
    SEUL = True

    text.Text("Temps/Distance :", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
              ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
              LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

    SCALE_X = 0.7
    SCALE_Y = 0
    LARGEUR = 200
    HAUTEUR = 50
    POSITION_X = -int(LARGEUR / 2)
    POSITION_Y = 185
    SCALE_WIDTH = 0
    SCALE_HEIGHT = 0
    COULEUR = constantes.BLACK
    ANTIALIAS = False
    COULEUR_TEXTE = constantes.BLACK
    FONT = "Arial"
    TAILLE_FONT = 20
    CENTRE_X = False
    CENTRE_Y = True
    ARRIERE_PLAN = None
    ECART = 0
    BORDURE = 0  # rempli
    SEUL = True

    text.Text(suffix400gm, ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
              ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
              LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

    POSITION_Y += 55

    text.Text(suffix400hgm, ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
              ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
              LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

    POSITION_Y += 55

    text.Text(suffixcigm, ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
              ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
              LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

    if stype == "Global":
        SCALE_X = 0.5
        SCALE_Y = 0
        LARGEUR = 580
        HAUTEUR = 10
        POSITION_X = - int(LARGEUR / 2)
        POSITION_Y = 380
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.BLACK
        ANTIALIAS = False
        COULEUR_TEXTE = constantes.RED if connection.connected is False else constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 20
        CENTRE_X = True
        CENTRE_Y = False
        ARRIERE_PLAN = None
        ECART = 1
        BORDURE = 0  # rempli
        SEUL = True

        text_to_dislay = \
            "Vos statistiques ne peuvent être envoyées car vous" \
                if not connection.connected \
                else "Connecté en tant que " + connection.username + "."
        text.Text(
            text_to_dislay,
            ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
            ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
            LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        # TODO: Temporaire en attendant d'avoir le /n dans Text()
        if not connection.connected:
            POSITION_Y += 20

            text.Text(
                "n'êtes connecté à aucun compte. Vous pouvez créér un compte sur",
                ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

            POSITION_Y += 20

            text.Text(
                constantes.WEBSITE_URI + "register et vous connecter",
                ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

            POSITION_Y += 20

            text.Text(
                "à ce dèrnier depuis le menu Paramètres.",
                ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


def login(bouton_connection):
    textbox_nom = textbox.Textbox.getTextboxes()[0]
    textbox_mdp = textbox.Textbox.getTextboxes()[1]

    textbox_nom.boxbordercolor = constantes.BLACK
    textbox_mdp.boxbordercolor = constantes.BLACK

    error = None

    if len(textbox_nom.text) >= 3:
        if len(textbox_mdp.text) >= 3:

            bouton_connection.visible = False

            ANTIALIAS = True
            COULEUR = constantes.BLACK
            FONT = "Arial"
            TAILLE_FONT = 22
            CENTRE_X = True
            CENTRE_Y = True
            ARRIERE_PLAN = None
            ECART = 0
            SEUL = True
            LARGEUR = 300
            HAUTEUR = 50
            POSITION_X = 100
            POSITION_Y = 100
            SCALE_X = 0
            SCALE_Y = 0
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = constantes.WHITE
            BORDURE = 0

            text.Text("Connexion en cours...", ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                      ECART,
                      SEUL, bouton_connection.parentsurface, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR,
                      SCALE_WIDTH, SCALE_HEIGHT,
                      COULEUR_ARRIERE, BORDURE)

            view.View.updatescreen()  # oui !

            # Par précaution, on se déconnecte d'abord :
            onlineconnector.OnlineConnector.current_connection.disconnect(True)
            # On essaye de se connecter
            occlass = onlineconnector.OnlineConnector(textbox_nom.text,
                                                      hashlib.sha1(textbox_mdp.text.encode('utf-8')).hexdigest(), True)
            try:
                occlass.connect()
                occlass.loadstatistiques()
                button.BConnexion.button1down(None)  # La connexion a eu lieu avec succès
            except pycurl.error:
                bouton_connection.visible = True
                error = "Une erreur est survenue lors de la connexion avec le serveur web"
            except BaseException:
                bouton_connection.visible = True
                if occlass.internet:
                    error = "Les identifiants semblent invalides !"
                else:
                    error = "Vous n'êtes pas connecté à internet !"
        else:
            textbox_mdp.boxbordercolor = constantes.RED
            error = "Mot de passe invalide"
    else:
        textbox_nom.boxbordercolor = constantes.RED
        error = "Nom d'utilisateur invalide"

    if error:
        if bouton_connection.errorobj:
            bouton_connection.errorobj.text = error
            return bouton_connection.errorobj
        else:
            ANTIALIAS = True
            COULEUR = constantes.RED
            FONT = "Arial"
            TAILLE_FONT = 22
            CENTRE_X = True
            CENTRE_Y = True
            ARRIERE_PLAN = None
            ECART = 0
            SEUL = True
            LARGEUR = 300
            HAUTEUR = 30
            POSITION_X = 100
            POSITION_Y = 150
            SCALE_X = 0
            SCALE_Y = 0
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = constantes.WHITE
            BORDURE = 0

            return text.Text(error, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,
                             SEUL, bouton_connection.parentsurface, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                             HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT,
                             COULEUR_ARRIERE, BORDURE)


def logout(bouton_connection):
    bouton_connection.visible = False

    ANTIALIAS = True
    COULEUR = constantes.BLACK
    FONT = "Arial"
    TAILLE_FONT = 22
    CENTRE_X = True
    CENTRE_Y = True
    ARRIERE_PLAN = None
    ECART = 0
    SEUL = True
    LARGEUR = 300
    HAUTEUR = 50
    POSITION_X = 100
    POSITION_Y = 100
    SCALE_X = 0
    SCALE_Y = 0
    SCALE_WIDTH = 0
    SCALE_HEIGHT = 0
    COULEUR_ARRIERE = constantes.WHITE
    BORDURE = 0

    text.Text("Déconnexion en cours...", ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,
              SEUL, bouton_connection.parentsurface, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR,
              SCALE_WIDTH, SCALE_HEIGHT,
              COULEUR_ARRIERE, BORDURE)

    # On le déconnecte
    onlineconnector.OnlineConnector.current_connection.disconnect(True)
    button.BConnexion.button1down(None)


def isvalidint(supposedint):
    var = True if (supposedint is not None and int(supposedint) is not None) else False
    return var
