import uielement
import model
import view
import controller
import statemanager

from uielements import image
from uielements import surface
from uielements import text
from uielements import checkbox
import constantes


class Button(uielement.UIelement):
    boutons = []

    """
    :param text - Le texte sur le bouton
    :param antialias - Y a-t-il l'anti-alias ou pas ?
    :param couleur_text - La couleur du texte
    :param font - Le font du texte
    :param font_size - La taille du font
    :param centeredx - Le texte est-il centré sur l'axe x ?
    :param centeredy - Le texte est-il centré sur l'axe y ?
    :param backgroundcolor - La couleur d'arrière plan de la surface sur laquelle le texte va être mis
    :param offset - Le nombre de pixel de décalage du texte sur l'axe x
    :param *UIargs - Tous les paramètres d'un élément graphique (voir classe "UIelement")
    """

    def __init__(self, text, antialias, couleur_text, font, font_size, centeredx, centeredy, backgroundcolor, offset,
                 *UIargs):

        uielement.UIelement.__init__(self, *UIargs, "Button")

        self.text = text
        self.antialias = antialias
        self.textcolor = couleur_text
        self.font = font
        self.fontsize = font_size
        self.textcenteredx = centeredx
        self.textcenteredy = centeredy
        self.backgroundcolor = backgroundcolor
        self.textoffset = offset
        self.clicking = False
        self.create()  # la référence est crée en appelant cela. ATTENTION: La référence est la surface sur laquelle le texte est dessinée

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

    def create(self): # pour créer l'élément graphique
        view.View.pygame.draw.rect(self.parentsurface, self.color, [self.x, self.y, self.width, self.height],
                              self.bordersize)
        text.Text.create(self)

    def __del__(self):
        if self in Button.boutons:
            Button.boutons.remove(self)  # on l'enlève de nos tables de boutons avant de le détruire
            self.remove()

    def getButtons(cls):
        return Button.boutons

    getButtons = classmethod(getButtons)


class BJouer(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        statemanager.StateManager.setstate(statemanager.StateEnum.PLAYERNUM)
        for button in list(Button.boutons):
            button.__del__()
        for surf in surface.Surface.getSurfaces():
            surf.__del__()

        POSITION_SURFACE = (0, 0)
        POSITION_X = 120
        POSITION_Y = 175
        LARGEUR = 400
        HAUTEUR = 175
        COULEUR = constantes.WHITE
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = True

        surface_boutons = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
                                HAUTEUR, COULEUR,
                                BORDURE)  # creation de la l'objet surface où on va mettre le titire et l'image du jeu

        POSITION_SURFACE = (POSITION_X, POSITION_Y)
        POSITION_X = 0
        POSITION_Y = 0
        LARGEUR = 400
        HAUTEUR = 50
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        B1Joueur("1 joueur", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                              ECART, surface_boutons.referance, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
                              HAUTEUR, COULEUR, BORDURE)
        POSITION_Y += 75
        B2Joueurs("2 joueurs", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                              ECART, surface_boutons.referance, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
                              HAUTEUR, COULEUR, BORDURE)

        POSITION_SURFACE = (0, 0)
        POSITION_X = 0
        POSITION_Y = 0
        LARGEUR = 100
        HAUTEUR = 50
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        BRetour("Retour", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                              ECART, view.View.screen, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
                              HAUTEUR, COULEUR, BORDURE)


class BParam(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        statemanager.StateManager.setstate(statemanager.StateEnum.SETTINGS_MENU)
        for button in list(Button.boutons):
            button.__del__()
        for surf in surface.Surface.getSurfaces():
            surf.__del__()

        POSITION_SURFACE = (0, 0)
        POSITION_X = 0
        POSITION_Y = 0
        LARGEUR = 100
        HAUTEUR = 50
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        BRetour("Retour", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                              ECART, view.View.screen, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
                              HAUTEUR, COULEUR, BORDURE)


class BStats(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        statemanager.StateManager.setstate(statemanager.StateEnum.STATS_MENU)
        for button in list(Button.boutons):
            button.__del__()
        for surf in surface.Surface.getSurfaces():
            surf.__del__()

        POSITION_SURFACE = (0, 0)
        POSITION_X = 0
        POSITION_Y = 0
        LARGEUR = 100
        HAUTEUR = 50
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        BRetour("Retour", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                              ECART, view.View.screen, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
                              HAUTEUR, COULEUR, BORDURE)


class B1Joueur(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        statemanager.StateManager.setstate(statemanager.StateEnum.MAP_AND_DIFF)
        for button in list(Button.boutons):
            button.__del__()
        for surf in surface.Surface.getSurfaces():
            surf.__del__()


        POSITION_SURFACE = (0, 0)
        POSITION_X = 50
        POSITION_Y = 100
        LARGEUR = 200
        HAUTEUR = 200
        COULEUR = constantes.WHITE
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = True

        surface_carte = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
                                HAUTEUR, COULEUR,
                                BORDURE)  # creation de la l'objet surface où on va mettre les choix de cartes


        POSITION_SURFACE = (POSITION_X, POSITION_Y)
        POSITION_X = 0
        POSITION_Y = 0
        LARGEUR = LARGEUR
        HAUTEUR = 50
        COULEUR = constantes.BLACK
        BOXSIZE = 30
        ANTIALIAS = False
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = False
        CENTRE_Y = True
        ARRIERE_PLAN = None
        ECART = 10
        BORDURE = 3  # rempli

        check_jo = checkbox.Checkbox(BOXSIZE, "Jeux Olympiques", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,surface_carte.referance, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR, HAUTEUR, COULEUR, BORDURE)
        POSITION_Y += 75
        check_athenes = checkbox.Checkbox(BOXSIZE, "Athènes", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,surface_carte.referance, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR, HAUTEUR, COULEUR, BORDURE)
        POSITION_Y += 75
        check_foret = checkbox.Checkbox(BOXSIZE, "Forêt", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,surface_carte.referance, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR, HAUTEUR, COULEUR, BORDURE)


        POSITION_SURFACE = (0, 0)
        POSITION_X = 0
        POSITION_Y = 0
        LARGEUR = 100
        HAUTEUR = 50
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        BRetour("Retour", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                              ECART, view.View.screen, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
                              HAUTEUR, COULEUR, BORDURE)



class B2Joueurs(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        statemanager.StateManager.setstate(statemanager.StateEnum.MAP_AND_DIFF)
        for button in list(Button.boutons):
            button.__del__()
        for surf in surface.Surface.getSurfaces():
            surf.__del__()

        POSITION_SURFACE = (0, 0)
        POSITION_X = 0
        POSITION_Y = 0
        LARGEUR = 100
        HAUTEUR = 50
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        BRetour("Retour", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                              ECART, view.View.screen, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
                              HAUTEUR, COULEUR, BORDURE)


menu_states = [  # les états du jeu qui font retourner au menu principale lorsqu'on clique sur retour
    statemanager.StateEnum.PLAYERNUM,
    statemanager.StateEnum.STATS_MENU,
    statemanager.StateEnum.SETTINGS_MENU,
]

class BRetour(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        for button in list(Button.boutons):
            button.__del__()
        for surf in surface.Surface.getSurfaces():
            surf.__del__()

        game_state = statemanager.StateManager.getstate()

        if game_state in menu_states:
            model.Model.endintro()  # bon, ce n'est pas la fin de l'intro mais c'est tellement bien adapté pour !
        elif game_state == statemanager.StateEnum.MAP_AND_DIFF:
            BJouer.button1down(None)  # pas sûr que c'est super bien de faire ca. Mais en réalité, c'est comme si on avait cliqué sur jouer...
