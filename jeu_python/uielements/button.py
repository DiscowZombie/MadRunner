import uielement
import model
import view
import controller
import statemanager

from coregame import coregame as coregame

from uielements import surface
from uielements import text
from uielements import checkbox

import constantes
import functions


class Button(uielement.UIelement):
    boutons = []

    """
    :param text - Le texte sur le bouton
    :param antialias - Y a-t-il l'anti-alias ou pas ?
    :param couleur_text - La couleur du texte
    :param backgroundtextcolor - La couleur de l'arrère plan du texte
    :param font - Le font du texte
    :param font_size - La taille du font
    :param centeredx - Le texte est-il centré sur l'axe x ?
    :param centeredy - Le texte est-il centré sur l'axe y ?
    :param backgroundcolor - La couleur d'arrière plan de la surface sur laquelle le texte va être mis
    :param offset - Le nombre de pixel de décalage du texte sur l'axe x
    :param *UIargs - Tous les paramètres d'un élément graphique (voir classe "UIelement")
    """

    def __init__(self, textb, antialias, couleur_text, backgroundtextcolor,  font, font_size, centeredx, centeredy, backgroundcolor, offset,
                 *UIargs):

        uielement.UIelement.__init__(self, *UIargs, "Button")

        self.text = textb
        self.antialias = antialias
        self.textcolor = couleur_text
        self.backgroundtextcolor = backgroundtextcolor
        self.font = font
        self.fontsize = font_size
        self.textcenteredx = centeredx
        self.textcenteredy = centeredy
        self.backgroundcolor = backgroundcolor
        self.textoffset = offset
        self.clicking = False
        self.textobj = text.Text(textb, antialias, couleur_text, font, font_size, centeredx, centeredy, backgroundtextcolor,
                                 offset, False, *UIargs)
        self.referance = self.create()  # la référence  est crée en appelant cela. ATTENTION: La référence est la surface sur laquelle le texte est dessinée, et il y a aussi l'attribut "rectreferance" qui est une référance vers le rectangle du bouton

        Button.boutons.append(self)

    def getmousein(self):
        return self.ismousein

    def setmousein(self, isin):
        self.ismousein = isin
        if isin:
            # vérifie si on est en train de cliquer dessus
            if controller.Controller.getpressingbuttons()["Mouse1"]:
                self.button1down()

    mousein = property(getmousein, setmousein)

    def create(self):  # pour créer l'élément graphique
        parentsurface = self.parentsurface
        referance = parentsurface.referance
        rectangle = view.View.pygame.draw.rect(
            self.parentsurface.referance,
            self.color,
            [referance.get_width() * self.scalex + self.x, referance.get_height() * self.scaley + self.y,
             referance.get_width() * self.scalew + self.width, referance.get_height() * self.scaleh + self.height],
            self.bordersize
        )
        self.textobj.create()
        return rectangle

    def draw(self):
        self.create()

    def __del__(self):
        self.textobj.__del__()
        if self in Button.boutons:
            Button.boutons.remove(self)  # on l'enlève de nos tables de boutons avant de le détruire
        self.remove()

    def getButtons(cls):
        return Button.boutons

    getButtons = classmethod(getButtons)


class BJouer(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(
            self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        statemanager.StateManager.setstate(statemanager.StateEnum.PLAYERNUM)
        functions.delete_menu_obj()

        SCALE_X = 0.5
        SCALE_Y = 0.5
        LARGEUR = 400
        HAUTEUR = 175
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        POSITION_X = - int(LARGEUR / 2)
        POSITION_Y = - int(HAUTEUR / 2)
        COULEUR = constantes.WHITE
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = True

        surface_boutons = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X,
                                          SCALE_Y, LARGEUR,
                                          HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = 400
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        ARRIERE_PLAN_TEXTE = COULEUR
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        B1Joueur("1 joueur", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                 ECART, surface_boutons, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                 HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        POSITION_Y += 75
        B2Joueurs("2 joueurs", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                  ECART, surface_boutons, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                  HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = 100
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        ARRIERE_PLAN_TEXTE = COULEUR
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        BRetour("Retour", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


class BParam(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(
            self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        statemanager.StateManager.setstate(statemanager.StateEnum.SETTINGS_MENU)
        functions.delete_menu_obj()

        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = 100
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        ARRIERE_PLAN_TEXTE = COULEUR
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        BRetour("Retour", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


class BStats(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(
            self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        statemanager.StateManager.setstate(statemanager.StateEnum.STATS_MENU)
        functions.delete_menu_obj()

        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = 100
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        ARRIERE_PLAN_TEXTE = COULEUR
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        BRetour("Retour", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


class B1Joueur(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(
            self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        statemanager.StateManager.setstate(statemanager.StateEnum.MAP_AND_DIFF)
        functions.delete_menu_obj()

        SCALE_X = 1/6
        SCALE_Y = 0.5
        LARGEUR = 175
        HAUTEUR = 250
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        POSITION_X = - int(LARGEUR / 2)
        POSITION_Y = - int(HAUTEUR / 2)
        COULEUR = constantes.WHITE
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = True

        surface_carte = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X,
                                        SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                        BORDURE)  # creation de la l'objet surface où on va mettre les choix de cartes

        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = LARGEUR
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.BLACK
        ANTIALIAS = False
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 28
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = None
        ECART = 0
        BORDURE = 0  # rempli
        SEUL = True

        texte_carte = text.Text("Carte :", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                                ARRIERE_PLAN, ECART, SEUL, surface_carte, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                                LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X = 0
        POSITION_Y = 50
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = LARGEUR
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.BLACK
        BOXSIZE = 30
        ANTIALIAS = False
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 20
        CENTRE_X = False
        CENTRE_Y = True
        ARRIERE_PLAN = None
        ECART = 10
        BORDURE = 3

        check_jo = checkbox.Checkbox(BOXSIZE, "Jeux Olympiques", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X,
                                     CENTRE_Y, ARRIERE_PLAN, ECART, surface_carte, POSITION_X, POSITION_Y, SCALE_X,
                                     SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        check_jo.check()
        POSITION_Y += 75
        check_athenes = checkbox.Checkbox(BOXSIZE, "Athènes", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X,
                                          CENTRE_Y, ARRIERE_PLAN, ECART, surface_carte, POSITION_X, POSITION_Y, SCALE_X,
                                          SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        POSITION_Y += 75
        check_foret = checkbox.Checkbox(BOXSIZE, "Forêt", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X,
                                        CENTRE_Y, ARRIERE_PLAN, ECART, surface_carte, POSITION_X, POSITION_Y, SCALE_X,
                                        SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        checkbox.Checkbox.linkcheckboxes(check_jo, check_athenes,
                                         check_foret)  # ces checbox sont liés, càd, si l'un se fait coché, les autres seront décochés

        SCALE_X = 0.5
        SCALE_Y = 0.5
        LARGEUR = 175
        HAUTEUR = 250
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        POSITION_X = - int(LARGEUR / 2)
        POSITION_Y = - int(HAUTEUR / 2)
        COULEUR = constantes.WHITE
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = True

        surface_mdj = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                                      LARGEUR,
                                      HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                      BORDURE)  # creation de la l'objet surface où on va mettre les choix de mode de jeu

        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = LARGEUR
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.BLACK
        ANTIALIAS = False
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 28
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = None
        ECART = 0
        BORDURE = 0  # rempli
        SEUL = True

        texte_mdj = text.Text("Mode de jeu :", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                              ARRIERE_PLAN, ECART, SEUL, surface_mdj, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                              HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X = 0
        POSITION_Y = 50
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = LARGEUR
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.BLACK
        BOXSIZE = 30
        ANTIALIAS = False
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 20
        CENTRE_X = False
        CENTRE_Y = True
        ARRIERE_PLAN = None
        ECART = 10
        BORDURE = 3

        check_400m = checkbox.Checkbox(BOXSIZE, "400m", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                                       ARRIERE_PLAN, ECART, surface_mdj, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                                       LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        check_400m.check()
        POSITION_Y += 75
        check_400m_haie = checkbox.Checkbox(BOXSIZE, "400m haie", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X,
                                            CENTRE_Y, ARRIERE_PLAN, ECART, surface_mdj, POSITION_X, POSITION_Y, SCALE_X,
                                            SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        POSITION_Y += 75
        check_course_inf = checkbox.Checkbox(BOXSIZE, "Course infinie", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT,
                                             CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART, surface_mdj, POSITION_X,
                                             POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT,
                                             COULEUR, BORDURE)

        checkbox.Checkbox.linkcheckboxes(check_400m, check_400m_haie,
                                         check_course_inf)  # ces checbox sont liés, càd, si l'un se fait coché, les autres seront décochés

        SCALE_X = 5/6
        SCALE_Y = 0.5
        LARGEUR = 175
        HAUTEUR = 250
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        POSITION_X = - int(LARGEUR / 2)
        POSITION_Y = - int(HAUTEUR / 2)
        COULEUR = constantes.WHITE
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = True

        surface_diff = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                                       LARGEUR,
                                       HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                       BORDURE)  # creation de la l'objet surface où on va mettre les choix de difficultés

        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = LARGEUR
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.BLACK
        ANTIALIAS = False
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 28
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = None
        ECART = 0
        BORDURE = 0  # rempli
        SEUL = True

        texte_diff = text.Text("Difficulté :", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                               ARRIERE_PLAN, ECART, SEUL, surface_diff, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                               LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X = 0
        POSITION_Y = 50
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = LARGEUR
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.BLACK
        BOXSIZE = 30
        ANTIALIAS = False
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 20
        CENTRE_X = False
        CENTRE_Y = True
        ARRIERE_PLAN = None
        ECART = 10
        BORDURE = 3

        check_facile = checkbox.Checkbox(BOXSIZE, "Facile", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X,
                                         CENTRE_Y, ARRIERE_PLAN, ECART, surface_diff, POSITION_X, POSITION_Y, SCALE_X,
                                         SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        POSITION_Y += 75
        check_moyen = checkbox.Checkbox(BOXSIZE, "Moyen", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X,
                                        CENTRE_Y, ARRIERE_PLAN, ECART, surface_diff, POSITION_X, POSITION_Y, SCALE_X,
                                        SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        check_moyen.check()
        POSITION_Y += 75
        check_difficile = checkbox.Checkbox(BOXSIZE, "Difficile", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X,
                                            CENTRE_Y, ARRIERE_PLAN, ECART, surface_diff, POSITION_X, POSITION_Y,
                                            SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                            BORDURE)

        checkbox.Checkbox.linkcheckboxes(check_facile, check_moyen,
                                         check_difficile)  # ces checbox sont liés, càd, si l'un se fait coché, les autres seront décochés

        SCALE_X = 1
        SCALE_Y = 1
        LARGEUR = 125
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        POSITION_X = - LARGEUR
        POSITION_Y = - HAUTEUR
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        ARRIERE_PLAN_TEXTE = COULEUR
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        BCommencer("Commencer", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                   ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                   HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = 100
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        ARRIERE_PLAN_TEXTE = COULEUR
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        BRetour("Retour", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


class B2Joueurs(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(
            self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        statemanager.StateManager.setstate(statemanager.StateEnum.MAP_AND_DIFF)
        functions.delete_menu_obj()

        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = 100
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        ARRIERE_PLAN_TEXTE = COULEUR
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        BRetour("Retour", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


class BCommencer(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self):
        # TODO: Seulement pour le debug
        carte = "jeux_olympiques"
        modejeu = "400m"
        level = "difficile"
        cgame = coregame.CoreGame(carte, modejeu, level)
        cgame.loop()


menu_states = [  # les états du jeu qui font retourner au menu principale lorsqu'on clique sur retour
    statemanager.StateEnum.PLAYERNUM,
    statemanager.StateEnum.STATS_MENU,
    statemanager.StateEnum.SETTINGS_MENU,
]


class BRetour(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(
            self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        functions.delete_menu_obj()

        game_state = statemanager.StateManager.getstate()

        if game_state in menu_states:
            model.Model.endintro()  # bon, ce n'est pas la fin de l'intro mais c'est tellement bien adapté pour !
        elif game_state == statemanager.StateEnum.MAP_AND_DIFF:
            BJouer.button1down(None)  # pas sûr que c'est super bien de faire ca. Mais en réalité, c'est comme si on avait cliqué sur jouer...

class BPause(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self):
        coregame.CoreGame.pause = not coregame.CoreGame.pause
