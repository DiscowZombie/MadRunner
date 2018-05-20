import pygame
import webbrowser

import uielement
import model
import view
import statemanager
import userstatistics

from coregame import coregame as coregame

from uielements import surface
from uielements import text
from uielements import checkbox
from uielements import tab
from uielements import textbox

import constantes
import functions
import onlineconnector
import settings


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

    def __init__(self, textb, antialias, couleur_text, backgroundtextcolor, font, font_size, centeredx, centeredy,
                 offset, *UIargs):

        uielement.UIelement.__init__(self, *UIargs, "Button")

        self.text = textb
        self.antialias = antialias
        self.textcolor = couleur_text
        self.backgroundtextcolor = backgroundtextcolor
        self.font = font
        self.fontsize = font_size
        self.textcenteredx = centeredx
        self.textcenteredy = centeredy
        self.textoffset = offset
        self.clicking = False  # va servir plus tard
        self.ismousein = False
        self.hoversound = pygame.mixer.Sound(functions.resource_path("assets\sounds\hover.ogg"))
        self.hoversound.set_volume(0.1)
        self.clicksound = pygame.mixer.Sound(functions.resource_path("assets\sounds\click.ogg"))
        self.clicksound.set_volume(0.4)
        self.textobj = text.Text(textb, antialias, couleur_text, font, font_size, centeredx, centeredy,
                                 backgroundtextcolor, offset, False, *UIargs)
        self.referance = self.create()  # ATTENTION: La référence est la surface sur laquelle le rectangle du bouton est dessiné

        Button.boutons.append(self)

    def getmousein(self):
        return self.ismousein

    def setmousein(self, isin):
        if isin and not self.ismousein:
            self.hoversound.play()
        self.ismousein = isin

    def click(self):
        self.clicking = True

    def unclick(self):
        self.clicksound.play()
        self.clicking = False
        self.button1click()

    mousein = property(getmousein, setmousein)

    def create(self):  # pour créer l'élément graphique
        parentsurface = self.parentsurface
        if self.visible and self.color:
            if self.mousein:
                if self.clicking:
                    rect_color = (self.color[0] + 20, self.color[1] + 20, self.color[2] + 20)
                else:
                    rect_color = (self.color[0] - 30, self.color[1] - 30, self.color[2] - 30)
            else:
                rect_color = self.color
            rect_color = list(rect_color)

            i = 0
            for colour in rect_color:  # vérifie que les composants de la couleur n'excèdent pas 255 ou ne sont pas inférieurs à 0
                if colour > 255:
                    colour = 255
                elif colour < 0:
                    colour = 0
                rect_color[i] = colour
                i += 1

            rectangle = pygame.draw.rect(
                parentsurface.referance,
                tuple(rect_color),
                [parentsurface.abswidth * self.scalex + self.x, parentsurface.absheight * self.scaley + self.y,
                 parentsurface.abswidth * self.scalew + self.width,
                 parentsurface.absheight * self.scaleh + self.height],
                self.bordersize
            )
        else:
            rectangle = None
        self.textobj.referance = self.textobj.create()
        return rectangle

    def draw(self):
        self.referance = self.create()

    def unreferance(self):
        Button.boutons.remove(self)
        self.remove()

    @classmethod
    def getButtons(cls):
        return Button.boutons


class BJouer(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(
            self):  # Défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        B1Joueur(functions.translate("1player"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                 CENTRE_X, CENTRE_Y,
                 ECART, surface_boutons, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                 HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        POSITION_Y += 75

        """
        B2Joueurs(functions.translate("2players"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                  ECART, surface_boutons, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                  HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)"""

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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BRetour(functions.translate("return"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                CENTRE_X, CENTRE_Y,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


class BParam(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        statemanager.StateManager.setstate(statemanager.StateEnum.SETTINGS_MENU)
        functions.delete_menu_obj()

        SCALE_X = 0.5
        SCALE_Y = 0.5
        LARGEUR = 400
        HAUTEUR = 200
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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BConnexion(functions.translate("login/register"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT,
                   TAILLE_FONT, CENTRE_X, CENTRE_Y,
                   ECART, surface_boutons, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                   HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        POSITION_Y += 75
        BLangue(functions.translate("language"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                CENTRE_X, CENTRE_Y,
                ECART, surface_boutons, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        POSITION_Y += 75
        BUpdate(functions.translate("update"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                CENTRE_X, CENTRE_Y,
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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BRetour(functions.translate("return"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                CENTRE_X, CENTRE_Y,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


class BUpdate(Button):

    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        statemanager.StateManager.setstate(statemanager.StateEnum.UPDATE_MENU)
        functions.delete_menu_obj()

        model_obj = model.Model.model

        if model_obj.latest_version_got:
            if model_obj.version == model_obj.latest_version:
                ANTIALIAS = True
                COULEUR = constantes.BLACK
                FONT = "Arial"
                TAILLE_FONT = 24
                CENTRE_X = True
                CENTRE_Y = True
                ARRIERE_PLAN = None
                ECART = 0
                SEUL = True
                LARGEUR = 550
                HAUTEUR = 30
                POSITION_X = - int(LARGEUR / 2)
                POSITION_Y = - int(HAUTEUR / 2)
                SCALE_X = 0.5
                SCALE_Y = 0.5
                SCALE_WIDTH = 0
                SCALE_HEIGHT = 0
                COULEUR_ARRIERE = constantes.WHITE
                BORDURE = 0

                text.Text(functions.translate("has_update"), ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                          ARRIERE_PLAN, ECART,
                          SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                          HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)
            else:
                ANTIALIAS = True
                COULEUR = constantes.RED
                FONT = "Arial"
                TAILLE_FONT = 24
                CENTRE_X = True
                CENTRE_Y = True
                ARRIERE_PLAN = None
                ECART = 0
                SEUL = True
                LARGEUR = 550
                HAUTEUR = 30
                POSITION_X = - int(LARGEUR / 2)
                POSITION_Y = - HAUTEUR
                SCALE_X = 0.5
                SCALE_Y = 0.5
                SCALE_WIDTH = 0
                SCALE_HEIGHT = 0
                COULEUR_ARRIERE = constantes.WHITE
                BORDURE = 0

                text.Text(functions.translate("hasnt_update"), ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X,
                          CENTRE_Y, ARRIERE_PLAN, ECART,
                          SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                          HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)
                POSITION_Y += HAUTEUR
                debut_texte = text.Text(functions.translate("download_latest") + " ", ANTIALIAS, COULEUR, FONT,
                                        TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,
                                        SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                        HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

                COULEUR = None
                COULEUR_TEXTE = constantes.LIGHT_BLUE
                ARRIERE_PLAN_TEXTE = None
                CENTRE_X = False

                fin_texte = BRedirect(constantes.WEBSITE_URI, functions.translate("here"), ANTIALIAS, COULEUR_TEXTE,
                                      ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                                      ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                      HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
                fin_texte.width = fin_texte.textobj.textreferance.size(fin_texte.text)[0]
                current_x = functions.centretexte(debut_texte.textreferance.size(debut_texte.text),
                                                  (debut_texte.abswidth, debut_texte.absheight))[0]
                new_x = functions.centretexte(debut_texte.textreferance.size(debut_texte.text + fin_texte.text),
                                              (debut_texte.abswidth, debut_texte.absheight))[0]
                debut_texte.originalx += new_x - current_x
                fin_texte.x = debut_texte.x + new_x - current_x + debut_texte.textreferance.size(debut_texte.text)[0]
        else:
            ANTIALIAS = True
            COULEUR = constantes.RED
            FONT = "Arial"
            TAILLE_FONT = 24
            CENTRE_X = True
            CENTRE_Y = True
            ARRIERE_PLAN = None
            ECART = 0
            SEUL = True
            LARGEUR = 550
            HAUTEUR = 30
            POSITION_X = - int(LARGEUR / 2)
            POSITION_Y = - int(HAUTEUR / 2)
            SCALE_X = 0.5
            SCALE_Y = 0.5
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = constantes.WHITE
            BORDURE = 0

            text.Text(functions.translate("update_error"), ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                      ARRIERE_PLAN, ECART,
                      SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                      HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BRetour(functions.translate("return"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                CENTRE_X, CENTRE_Y,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


class BLangue(Button):

    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        statemanager.StateManager.setstate(statemanager.StateEnum.LANGUAGE_MENU)
        functions.delete_menu_obj()

        LARGEUR = 400
        HAUTEUR = 125
        POSITION_X = -int(LARGEUR / 2)
        POSITION_Y = -int(HAUTEUR / 2)
        SCALE_X = 0.5
        SCALE_Y = 0.5
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.WHITE
        BORDURE = 0
        ALPHA = 255
        CONVERT_ALPHA = True

        surface_lang = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X,
                                       SCALE_Y, LARGEUR,
                                       HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                       BORDURE)  # creation de la l'objet surface où on va mettre les choix de langue

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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BLanguage("en", "English", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                  ECART, surface_lang, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                  HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        POSITION_Y += 75
        BLanguage("fr", "Français", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                  ECART, surface_lang, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BRetour(functions.translate("return"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                CENTRE_X, CENTRE_Y,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


class BLanguage(Button):

    def __init__(self, language_id, *arguments):
        Button.__init__(self, *arguments)
        self.language = language_id

    def button1click(self):
        current_settings = settings.SettingsManager.current_settings
        current_settings["game_settings"]["language"] = self.language

        settings.SettingsManager.update_settings()
        BRetour.button1click(None)


class BConnexion(Button):

    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        statemanager.StateManager.setstate(statemanager.StateEnum.CONNEXION_MENU)
        functions.delete_menu_obj()

        LARGEUR = 500
        HAUTEUR = 225
        POSITION_X = -int(LARGEUR / 2)
        POSITION_Y = -int(HAUTEUR / 2)
        SCALE_X = 0.5
        SCALE_Y = 0.5
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.WHITE
        BORDURE = 0
        ALPHA = 255
        CONVERT_ALPHA = True

        surface_box = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X,
                                      SCALE_Y, LARGEUR,
                                      HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                      BORDURE)  # creation de la l'objet surface où on va mettre les textbox et autres

        connected = onlineconnector.OnlineConnector.current_connection.connected

        if connected:
            TEXTE_BOUTON = "logout"

            ANTIALIAS = True
            COULEUR = constantes.BLACK
            FONT = "Arial"
            TAILLE_FONT = 22
            CENTRE_X = True
            CENTRE_Y = True
            ARRIERE_PLAN = None
            ECART = 0
            SEUL = True
            LARGEUR = 500
            HAUTEUR = 30
            POSITION_X = 0
            POSITION_Y = 0
            SCALE_X = 0
            SCALE_Y = 0
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = constantes.WHITE
            BORDURE = 0

            text.Text(functions.translate("logged_as") + " :", ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X,
                      CENTRE_Y, ARRIERE_PLAN,
                      ECART,
                      SEUL, surface_box, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH,
                      SCALE_HEIGHT,
                      COULEUR_ARRIERE, BORDURE)

            NAME = onlineconnector.OnlineConnector.current_connection.username
            ANTIALIAS = True
            COULEUR = constantes.BLACK
            FONT = "Arial"
            TAILLE_FONT = 26
            CENTRE_X = True
            CENTRE_Y = True
            ARRIERE_PLAN = None
            ECART = 0
            SEUL = True
            LARGEUR = 500
            HAUTEUR = 50
            POSITION_X = 0
            POSITION_Y = 50
            SCALE_X = 0
            SCALE_Y = 0
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = constantes.WHITE
            BORDURE = 0

            text.Text(NAME, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,
                      SEUL, surface_box, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH,
                      SCALE_HEIGHT,
                      COULEUR_ARRIERE, BORDURE)
        else:
            TEXTE_BOUTON = "login"

            ANTIALIAS = True
            COULEUR = constantes.BLACK
            FONT = "Arial"
            TAILLE_FONT = 22
            CENTRE_X = True
            CENTRE_Y = True
            ARRIERE_PLAN = None
            ECART = 0
            SEUL = True
            LARGEUR = 175
            HAUTEUR = 30
            POSITION_X = 0
            POSITION_Y = 0
            SCALE_X = 0
            SCALE_Y = 0
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = constantes.WHITE
            BORDURE = 0

            text.Text(functions.translate("username") + " :", ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                      ARRIERE_PLAN,
                      ECART,
                      SEUL, surface_box, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH,
                      SCALE_HEIGHT,
                      COULEUR_ARRIERE, BORDURE)

            POSITION_Y += 50

            text.Text(functions.translate("password") + " :", ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                      ARRIERE_PLAN, ECART,
                      SEUL, surface_box, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH,
                      SCALE_HEIGHT,
                      COULEUR_ARRIERE, BORDURE)

            POSITION_X = 185
            POSITION_Y = 0
            SCALE_X = 0
            SCALE_Y = 0
            LARGEUR = 315
            HAUTEUR = 30
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR = constantes.WHITE
            ANTIALIAS = True
            COULEUR_TEXTE = constantes.BLACK
            FONT = "Arial"
            TAILLE_FONT = 22
            CENTRE_X = False
            CENTRE_Y = True
            ECART = 3
            BOX_BORDER_SIZE = 2
            COULEUR_BORDURE = constantes.BLACK
            MAX_CHAR = 16
            MDP = False
            BORDURE = 0  # rempli

            textbox.Textbox(ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                            ECART, BOX_BORDER_SIZE, COULEUR_BORDURE, MAX_CHAR, MDP,
                            surface_box, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR,
                            SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

            POSITION_Y += 50
            MAX_CHAR = 32
            MDP = True

            textbox.Textbox(ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                            ECART, BOX_BORDER_SIZE, COULEUR_BORDURE, MAX_CHAR, MDP,
                            surface_box, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR,
                            SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

            ANTIALIAS = True
            COULEUR = constantes.BLACK
            FONT = "Arial"
            TAILLE_FONT = 20
            CENTRE_X = True
            CENTRE_Y = True
            ARRIERE_PLAN = None
            ECART = 0
            SEUL = True
            LARGEUR = 400
            HAUTEUR = 20
            POSITION_X = - int(LARGEUR / 2)
            POSITION_Y = 200
            SCALE_X = 0.5
            SCALE_Y = 0
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = constantes.WHITE
            BORDURE = 0

            debut_texte = text.Text(functions.translate("no_account") + " ", ANTIALIAS, COULEUR, FONT, TAILLE_FONT,
                                    CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,
                                    SEUL, surface_box, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR,
                                    SCALE_WIDTH,
                                    SCALE_HEIGHT,
                                    COULEUR_ARRIERE, BORDURE)

            COULEUR = None
            COULEUR_TEXTE = constantes.LIGHT_BLUE
            ARRIERE_PLAN_TEXTE = None
            CENTRE_X = False

            fin_texte = BRedirect(constantes.WEBSITE_URI + "register", functions.translate("here"), ANTIALIAS,
                                  COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                                  ECART, surface_box, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                  HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
            fin_texte.width = fin_texte.textobj.textreferance.size(fin_texte.text)[0]
            current_x = functions.centretexte(debut_texte.textreferance.size(debut_texte.text),
                                              (debut_texte.abswidth, debut_texte.absheight))[0]
            new_x = functions.centretexte(debut_texte.textreferance.size(debut_texte.text + fin_texte.text),
                                          (debut_texte.abswidth, debut_texte.absheight))[0]
            debut_texte.originalx += new_x - current_x
            fin_texte.x = debut_texte.x + new_x - current_x + debut_texte.textreferance.size(debut_texte.text)[0]

        POSITION_X = 100
        POSITION_Y = 100
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = 300
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BSeConnecter(functions.translate(TEXTE_BOUTON), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                     CENTRE_X, CENTRE_Y,
                     ECART, surface_box, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BRetour(functions.translate("return"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                CENTRE_X, CENTRE_Y,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


class BSeConnecter(Button):  # enfait, il permet aussi de se déconnecter si on déjà connecté

    def __init__(self, *arguments):
        Button.__init__(self, *arguments)
        self.errorobj = None

    def button1click(self):
        connected = onlineconnector.OnlineConnector.current_connection.connected

        if connected:
            self.errorobj = functions.logout(self)
        else:
            self.errorobj = functions.login(self)


class BRedirect(Button):
    def __init__(self, redirect_url, *arguments):
        Button.__init__(self, *arguments)
        self.redirect_url = redirect_url

    def button1click(self):
        webbrowser.open(self.redirect_url)


class BStats(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        statemanager.StateManager.setstate(statemanager.StateEnum.STATS_MENU)
        functions.delete_menu_obj()

        # La surface où se trouvent 2 boutons
        SCALE_X = 0.5
        SCALE_Y = 0.5
        LARGEUR = 400
        HAUTEUR = 125
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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BMeilleurScore(functions.translate("best_score"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT,
                       TAILLE_FONT, CENTRE_X,
                       CENTRE_Y,
                       ECART, surface_boutons, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                       HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_Y += 75

        BAutreStats(functions.translate("other"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                    CENTRE_X, CENTRE_Y,
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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BRetour(functions.translate("return"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                CENTRE_X, CENTRE_Y,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


class B1Joueur(Button):

    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        statemanager.StateManager.setstate(statemanager.StateEnum.MAP_AND_DIFF)
        functions.delete_menu_obj()

        SCALE_X = 1 / 6
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

        texte_carte = text.Text(functions.translate("map") + " :", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT,
                                CENTRE_X, CENTRE_Y,
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

        check_jo = checkbox.Checkbox(BOXSIZE, "Jeux Olympiques", functions.translate("olympic_games"), ANTIALIAS,
                                     COULEUR_TEXTE, FONT, TAILLE_FONT,
                                     CENTRE_X,
                                     CENTRE_Y, ARRIERE_PLAN, ECART, surface_carte, POSITION_X, POSITION_Y, SCALE_X,
                                     SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        check_jo.check()

        POSITION_Y += 75
        check_athenes = checkbox.Checkbox(BOXSIZE, "Athènes", functions.translate("athens"), ANTIALIAS, COULEUR_TEXTE,
                                          FONT, TAILLE_FONT,
                                          CENTRE_X,
                                          CENTRE_Y, ARRIERE_PLAN, ECART, surface_carte, POSITION_X, POSITION_Y,
                                          SCALE_X,
                                          SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        POSITION_Y += 75
        check_foret = checkbox.Checkbox(BOXSIZE, "Forêt", functions.translate("forest"), ANTIALIAS, COULEUR_TEXTE, FONT,
                                        TAILLE_FONT, CENTRE_X,
                                        CENTRE_Y, ARRIERE_PLAN, ECART, surface_carte, POSITION_X, POSITION_Y,
                                        SCALE_X,
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

        texte_mdj = text.Text(functions.translate("game_mode") + " :", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT,
                              CENTRE_X, CENTRE_Y,
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

        check_400m = checkbox.Checkbox(BOXSIZE, "400m", functions.translate("400m"), ANTIALIAS, COULEUR_TEXTE, FONT,
                                       TAILLE_FONT, CENTRE_X,
                                       CENTRE_Y,
                                       ARRIERE_PLAN, ECART, surface_mdj, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                                       LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        check_400m.check()
        POSITION_Y += 75
        check_400m_haie = checkbox.Checkbox(BOXSIZE, "400m haie", functions.translate("400m_hurdles"), ANTIALIAS,
                                            COULEUR_TEXTE, FONT, TAILLE_FONT,
                                            CENTRE_X,
                                            CENTRE_Y, ARRIERE_PLAN, ECART, surface_mdj, POSITION_X, POSITION_Y,
                                            SCALE_X,
                                            SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        POSITION_Y += 75
        check_course_inf = checkbox.Checkbox(BOXSIZE, "Course infinie", functions.translate("infinite_run"), ANTIALIAS,
                                             COULEUR_TEXTE, FONT,
                                             TAILLE_FONT,
                                             CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART, surface_mdj, POSITION_X,
                                             POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH,
                                             SCALE_HEIGHT,
                                             COULEUR, BORDURE)

        checkbox.Checkbox.linkcheckboxes(check_400m, check_400m_haie,
                                         check_course_inf)  # ces checbox sont liés, càd, si l'un se fait coché, les autres seront décochés

        SCALE_X = 5 / 6
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

        texte_diff = text.Text(functions.translate("difficulty") + " :", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT,
                               CENTRE_X, CENTRE_Y,
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

        check_facile = checkbox.Checkbox(BOXSIZE, "Facile", functions.translate("easy"), ANTIALIAS, COULEUR_TEXTE, FONT,
                                         TAILLE_FONT, CENTRE_X,
                                         CENTRE_Y, ARRIERE_PLAN, ECART, surface_diff, POSITION_X, POSITION_Y,
                                         SCALE_X,
                                         SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        POSITION_Y += 75
        check_moyen = checkbox.Checkbox(BOXSIZE, "Moyen", functions.translate("medium"), ANTIALIAS, COULEUR_TEXTE, FONT,
                                        TAILLE_FONT, CENTRE_X,
                                        CENTRE_Y, ARRIERE_PLAN, ECART, surface_diff, POSITION_X, POSITION_Y,
                                        SCALE_X,
                                        SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        check_moyen.check()
        POSITION_Y += 75
        check_difficile = checkbox.Checkbox(BOXSIZE, "Difficile", functions.translate("hard"), ANTIALIAS, COULEUR_TEXTE,
                                            FONT, TAILLE_FONT,
                                            CENTRE_X,
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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BCommencer(functions.translate("start"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                   CENTRE_X, CENTRE_Y,
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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BRetour(functions.translate("return"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                CENTRE_X, CENTRE_Y,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


"""
Mode deux joueurs :
class B2Joueurs(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(
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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BRetour(functions.translate("return"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)"""


class BCommencer(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        carte = None
        modejeu = None
        level = None

        for checkboxe in checkbox.Checkbox.getCheckboxes():
            if checkboxe.checked:
                if carte is None:
                    carte = checkboxe
                elif modejeu is None:
                    modejeu = checkboxe
                else:
                    level = checkboxe

        coregame.CoreGame(carte.name, modejeu.name, level.name)


class BMeilleurScore(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        statemanager.StateManager.setstate(statemanager.StateEnum.BEST_SCORE)
        functions.delete_menu_obj()

        # La surface où se trouvent les boutons "Personnel" et "Global"
        SCALE_X = 0.5
        SCALE_Y = 0
        LARGEUR = 400
        HAUTEUR = 55
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        POSITION_X = -int(LARGEUR / 2)
        POSITION_Y = 0
        COULEUR = constantes.WHITE
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = True

        surface_population = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X,
                                             SCALE_Y, LARGEUR,
                                             HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X = 0
        POSITION_Y = 5
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = 200
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 22
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN_SELECT = constantes.WHITE
        ARRIERE_PLAN_UNSELECT = COULEUR
        ECART = 0
        IMAGE = "assets/img/local.png"
        BORDURE = 0  # rempli

        tab_local = tab.TMeilleurScoreLocal("Personnel", functions.translate("personal"), ANTIALIAS, COULEUR_TEXTE,
                                            ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                                            CENTRE_X, CENTRE_Y,
                                            ARRIERE_PLAN_SELECT, ARRIERE_PLAN_UNSELECT,
                                            ECART, IMAGE, surface_population, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                                            LARGEUR,
                                            HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X += LARGEUR
        IMAGE = "assets/img/en ligne.png"

        tab_ligne = tab.TMeilleurScoreEnLigne("Global", functions.translate("global"), ANTIALIAS, COULEUR_TEXTE,
                                              ARRIERE_PLAN_TEXTE, FONT,
                                              TAILLE_FONT, CENTRE_X, CENTRE_Y,
                                              ARRIERE_PLAN_SELECT, ARRIERE_PLAN_UNSELECT,
                                              ECART, IMAGE, surface_population, POSITION_X, POSITION_Y, SCALE_X,
                                              SCALE_Y, LARGEUR,
                                              HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        tab.Tab.linktabs(tab_local, tab_ligne)
        tab_local.select(True)

        # La surface où se trouvent les boutons "facile" et "moyen" et "difficile"
        SCALE_X = 0.5
        SCALE_Y = 0
        LARGEUR = 450
        HAUTEUR = 55
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        POSITION_X = -int(LARGEUR / 2)
        POSITION_Y = 55
        COULEUR = constantes.WHITE
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = True

        surface_diff = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X,
                                       SCALE_Y, LARGEUR,
                                       HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X = 0
        POSITION_Y = 5
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = 150
        HAUTEUR = 50
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 22
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN_SELECT = constantes.WHITE
        ARRIERE_PLAN_UNSELECT = COULEUR
        ECART = 0
        IMAGE = None
        BORDURE = 0  # rempli

        tab_facile = tab.TFacile("Facile", functions.translate("easy"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE,
                                 FONT, TAILLE_FONT, CENTRE_X,
                                 CENTRE_Y,
                                 ARRIERE_PLAN_SELECT, ARRIERE_PLAN_UNSELECT,
                                 ECART, IMAGE, surface_diff, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                 HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X += LARGEUR

        tab_moyen = tab.TMoyen("Moyen", functions.translate("medium"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE,
                               FONT, TAILLE_FONT, CENTRE_X,
                               CENTRE_Y,
                               ARRIERE_PLAN_SELECT, ARRIERE_PLAN_UNSELECT,
                               ECART, IMAGE, surface_diff, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                               HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X += LARGEUR

        tab_difficile = tab.TDifficile("Difficile", functions.translate("hard"), ANTIALIAS, COULEUR_TEXTE,
                                       ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                                       CENTRE_X, CENTRE_Y,
                                       ARRIERE_PLAN_SELECT, ARRIERE_PLAN_UNSELECT,
                                       ECART, IMAGE, surface_diff, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                       HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        tab.Tab.linktabs(tab_facile, tab_moyen, tab_difficile)
        tab_moyen.select()

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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BRetour(functions.translate("return"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                CENTRE_X, CENTRE_Y,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


class BAutreStats(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        statemanager.StateManager.setstate(statemanager.StateEnum.AUTRE_STATS)
        functions.delete_menu_obj()
        stats_obj = userstatistics.UserStatistics.stats

        SCALE_X = 0.5
        SCALE_Y = 0
        LARGEUR = 200
        HAUTEUR = 30
        POSITION_X = -int(LARGEUR / 2)
        POSITION_Y = 25
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.BLACK
        ANTIALIAS = False
        COULEUR_TEXTE = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 18
        CENTRE_X = False
        CENTRE_Y = True
        ARRIERE_PLAN = None
        ECART = 0
        BORDURE = 0  # rempli
        SEUL = True

        text.Text(functions.translate("total_score") + ": " + str(int(stats_obj.score_total)), ANTIALIAS, COULEUR_TEXTE,
                  FONT, TAILLE_FONT,
                  CENTRE_X, CENTRE_Y,
                  ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                  LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_Y += 35

        text.Text(functions.translate("course_number") + ": " + str(stats_obj.nb_courses), ANTIALIAS, COULEUR_TEXTE,
                  FONT, TAILLE_FONT,
                  CENTRE_X, CENTRE_Y,
                  ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                  LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X += 35
        POSITION_Y += 30

        text.Text(functions.translate("failed_courses") + ": " + str(stats_obj.nb_courses_echouees), ANTIALIAS,
                  COULEUR_TEXTE, FONT, TAILLE_FONT,
                  CENTRE_X, CENTRE_Y,
                  ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                  LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X -= 35
        POSITION_Y += 35

        text.Text(functions.translate("jump_number") + ": " + str(stats_obj.nb_sauts), ANTIALIAS, COULEUR_TEXTE, FONT,
                  TAILLE_FONT, CENTRE_X,
                  CENTRE_Y,
                  ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                  LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_Y += 35

        text.Text(functions.translate("traveled_distance") + ": " + str(int(stats_obj.total_dist)) + " m", ANTIALIAS,
                  COULEUR_TEXTE, FONT,
                  TAILLE_FONT, CENTRE_X, CENTRE_Y,
                  ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                  LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_Y += 35

        text.Text(functions.translate("letters_number") + ": " + str(
            stats_obj.correct_letters + stats_obj.wrong_letters + stats_obj.missed_letters),
                  ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                  ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                  LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X += 35
        POSITION_Y += 30

        text.Text(functions.translate("correct_letters") + ": " + str(stats_obj.correct_letters), ANTIALIAS,
                  COULEUR_TEXTE, FONT, TAILLE_FONT,
                  CENTRE_X, CENTRE_Y,
                  ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                  LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_Y += 30

        text.Text(functions.translate("wrong_letters") + ": " + str(stats_obj.wrong_letters), ANTIALIAS, COULEUR_TEXTE,
                  FONT, TAILLE_FONT,
                  CENTRE_X, CENTRE_Y,
                  ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                  LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_Y += 30

        text.Text(functions.translate("missed_letters") + ": " + str(stats_obj.missed_letters), ANTIALIAS,
                  COULEUR_TEXTE, FONT, TAILLE_FONT,
                  CENTRE_X, CENTRE_Y,
                  ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                  LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_Y += 30

        precision = 100
        if stats_obj.wrong_letters + stats_obj.correct_letters > 0:
            precision = int((stats_obj.correct_letters / (stats_obj.wrong_letters + stats_obj.correct_letters)) * 100)

        text.Text(functions.translate("accuracy") + ": " + str(precision) + " %", ANTIALIAS, COULEUR_TEXTE, FONT,
                  TAILLE_FONT, CENTRE_X,
                  CENTRE_Y,
                  ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                  LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_X -= 35
        POSITION_Y += 35

        text.Text(functions.translate("crossed_hurdles") + ": " + str(stats_obj.haies_traversees), ANTIALIAS,
                  COULEUR_TEXTE, FONT, TAILLE_FONT,
                  CENTRE_X, CENTRE_Y,
                  ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                  LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_Y += 35

        text.Text(functions.translate("knocked_down_hurdles") + ": " + str(stats_obj.haies_renversees), ANTIALIAS,
                  COULEUR_TEXTE, FONT, TAILLE_FONT,
                  CENTRE_X, CENTRE_Y,
                  ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                  LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        POSITION_Y += 35

        text.Text(functions.translate("play_time") + ": " + functions.computeplaytime(stats_obj.temps_jeu), ANTIALIAS,
                  COULEUR_TEXTE, FONT,
                  TAILLE_FONT, CENTRE_X, CENTRE_Y,
                  ARRIERE_PLAN, ECART, SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                  LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

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
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ECART = 0
        BORDURE = 0  # rempli

        BRetour(functions.translate("return"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                CENTRE_X, CENTRE_Y,
                ECART, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)


class BRafraichir(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        try:
            onlineconnector.OnlineConnector.current_connection.loadstatistiques().join()
        except:
            return
        for tabb in tab.Tab.getTabs():
            if tabb.selected and tabb.name != "Global":
                functions.displaybestscore("Global", tabb.name)


class BYesUpdate(Button):

    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        functions.delete_menu_obj()
        webbrowser.open(constantes.WEBSITE_URI)
        model.Model.main_menu(True)


class BLaterUpdate(Button):

    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        functions.delete_menu_obj()
        model.Model.main_menu(True)


class BNoUpdate(Button):

    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        functions.delete_menu_obj()
        functions.ignore_update(model.Model.model.latest_version)
        model.Model.main_menu(True)


menu_states = [  # les états du jeu qui font retourner au menu principal lorsqu'on clique sur retour
    statemanager.StateEnum.PLAYERNUM,
    statemanager.StateEnum.STATS_MENU,
    statemanager.StateEnum.SETTINGS_MENU,
]


class BRetour(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        functions.delete_menu_obj()

        game_state = statemanager.StateManager.getstate()
        if game_state in menu_states:
            model.Model.main_menu(True)
        elif game_state == statemanager.StateEnum.MAP_AND_DIFF:
            BJouer.button1click(None)  # C'est comme si on avait cliqué sur jouer
        elif game_state == statemanager.StateEnum.BEST_SCORE or game_state == statemanager.StateEnum.AUTRE_STATS:
            BStats.button1click(None)  # C'est comme si on avait cliqué sur statistiques
        elif game_state == statemanager.StateEnum.CONNEXION_MENU or game_state == statemanager.StateEnum.LANGUAGE_MENU or game_state == statemanager.StateEnum.UPDATE_MENU:
            BParam.button1click(None)  # C'est comme si on avait cliqué sur paramètres


class BPause(Button):
    def __init__(self, *arguments):
        Button.__init__(self, *arguments)
        self.on = False  # est-ce en pause
        self.surface_pause = None  # n'existe que lorsque self.on est sur True

    def button1click(self):
        core = coregame.CoreGame.current_core
        if not core.started or core.finished:  # pas possible de faire pause avant que la partie aie commencée ou après la fin de la course
            return
        self.on = not self.on
        core.pause = self.on
        core.surface_boutons.visible = not self.on

        if self.on:

            LARGEUR = 300
            HAUTEUR = 150
            POSITION_X = - int(LARGEUR / 2)
            POSITION_Y = - int(HAUTEUR / 2)
            SCALE_X = 0.5
            SCALE_Y = 0.5
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR = constantes.LIGHT_GRAY
            BORDURE = 0
            ALPHA = 255
            CONVERT_ALPHA = False

            self.surface_pause = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y,
                                                 SCALE_X,
                                                 SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

            ANTIALIAS = True
            COULEUR = constantes.BLACK
            FONT = "Arial"
            TAILLE_FONT = 35
            CENTRE_X = True
            CENTRE_Y = False
            ARRIERE_PLAN = None
            ECART = 0
            SEUL = True
            LARGEUR = 280
            HAUTEUR = 75
            POSITION_X = 10
            POSITION_Y = 15
            SCALE_X = 0
            SCALE_Y = 0
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = constantes.WHITE
            BORDURE = 0

            text.Text(functions.translate("pause").upper(), ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                      ARRIERE_PLAN, ECART,
                      SEUL, self.surface_pause, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR,
                      SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

            POSITION_X = 10
            POSITION_Y = 105
            SCALE_X = 0
            SCALE_Y = 0
            LARGEUR = 280
            HAUTEUR = 35
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR = constantes.GRAY
            ANTIALIAS = True
            COULEUR_TEXTE = constantes.BLACK
            ARRIERE_PLAN_TEXTE = None
            FONT = "Arial"
            TAILLE_FONT = 24
            CENTRE_X = True
            CENTRE_Y = True
            ECART = 0
            BORDURE = 0  # rempli

            BRetourMenu(functions.translate("return_menu"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT,
                        TAILLE_FONT, CENTRE_X, CENTRE_Y,
                        ECART, self.surface_pause, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR,
                        SCALE_WIDTH,
                        SCALE_HEIGHT, COULEUR, BORDURE)
        else:
            self.surface_pause.unreferance()
            self.surface_pause = None


"""
Un bouton de retour au menu après la fin du jeu
"""


class BRetourMenu(Button):

    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1click(self):
        core = coregame.CoreGame.current_core
        if not core.finished:  # quitte depuis le menu pause
            core.end(False, True)
        core.unreferance()  # "efface" la partie
