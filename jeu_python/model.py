import view
import constantes
import statemanager
import uielement
import userstatistics
import functions as f

from uielements import text as text
from uielements import surface as surface
from uielements import button as button
from uielements import image as image
from uielements import checkbox as checkbox
from uielements import tab as tab
from uielements import textbox as textbox

from coregame import coregame as coregame


class Intro:

    def __init__(self):
        self.transparent = False  # devient True lorsque l'icône du jeu commence à devenir transparent

    def start(self):
        statemanager.StateManager.setstate(statemanager.StateEnum.INTRO)

        # état initial de la surface où on va mettre le logo et le titre du jeu
        LARGEUR = 0  # état final: 225
        HAUTEUR = 0  # état final: 225
        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0.5  # milieu de l'écran
        SCALE_Y = 0.5  # idem
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.WHITE
        BORDURE = 0  # rempli
        ALPHA = 0  # transparence
        CONVERT_ALPHA = False

        surface_intro = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X,
                                        SCALE_Y, LARGEUR,
                                        HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                        BORDURE)  # creation de la l'objet surface où on va mettre le titire et l'image du jeu

        # état intial de l'image du logo
        REPERTOIRE = "assets/img/menu_fond.png"
        LARGEUR = 0
        HAUTEUR = 0
        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0.3
        SCALE_WIDTH = 1
        SCALE_HEIGHT = 0.7
        COULEUR = constantes.WHITE
        BORDURE = 0

        image_intro = image.Image(REPERTOIRE, surface_intro, POSITION_X,
                                  POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                  BORDURE)

        # état initial du texte du jeu
        TEXTE = "Mad Runner"
        ANTIALIAS = True
        COULEUR = constantes.BLACK  # couleur du texte
        FONT = "Arial"
        TAILLE_FONT = 0
        CENTRE_X = True  # centré sur l'axe x
        CENTRE_Y = True  # centré sur l'axe y
        ARRIERE_PLAN = constantes.WHITE
        ECART = 0
        SEUL = True
        LARGEUR = 0
        HAUTEUR = 0
        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        SCALE_WIDTH = 1
        SCALE_HEIGHT = 0.3
        COULEUR_ARRIERE = constantes.WHITE
        BORDURE = 0

        texte_intro = text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,
                                SEUL,
                                surface_intro, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

        # et enfin, on fait une merveilleuse transition vers l'état final de l'image et du texte

        surface_intro.tween(
            1,
            [
                {
                    "name": "x",
                    "value": -112
                },
                {
                    "name": "y",
                    "value": -112
                },
                {
                    "name": "width",
                    "value": 225
                },
                {
                    "name": "height",
                    "value": 225
                },
                {
                    "name": "alpha",
                    "value": 255
                }
            ]
        )

        texte_intro.tween(
            1,
            [
                {
                    "name": "fontsize",
                    "value": 44
                }
            ]
        )

    def update(self):
        state_time = statemanager.StateManager.getstatetime()
        if state_time <= 3000:
            pass
        elif state_time <= 4000 and not self.transparent:
            self.transparent = True
            surfaceintro = surface.Surface.getSurfaces()[0]
            surfaceintro.tween(
                1,
                [
                    {
                        "name": "alpha",
                        "value": 0  # transparent
                    }
                ]
            )
        elif state_time >= 4500:
            statemanager.StateManager.setstate(statemanager.StateEnum.MAIN_MENU)
            surface.Surface.getSurfaces()[0].unreferance()
            delattr(Model.model, "intro")
            Model.main_menu()


class Model:
    model = None
    last_passed = 0

    def __init__(self):
        self.version = "1.1"
        self.latest_version_got = False  # la dernière version a-t-elle été obtenue ?
        self.latest_version = self.version  # va être vérifié à la prochaine ligne !
        f.set_latest_version()
        self.intro = Intro()
        self.update_reminded = False

        Model.model = self

    @classmethod
    def updatemodel(cls, passed):

        Model.last_passed = passed

        UIelements = uielement.UIelement.getUIelements()

        for classname in UIelements:  # on met à jour les position absolues des éléments graphiques en premier...
            for obj in UIelements[classname]:
                if obj.tweendata:  # tout d'abord, on calcule la nouvelle valeur des attributs qui sont transitionnés
                    obj.updatetween()
                    obj.tweendata["passed"] += passed / 1000
                    if obj.tweendata["passed"] >= obj.tweendata["duration"]:
                        obj.tweendata["passed"] = obj.tweendata["duration"]
                        obj.updatetween()
                        previous_tween_data = obj.tweendata
                        if obj.tweendata["endfunction"]:
                            obj.tweendata["endfunction"]()
                        if obj.tweendata == previous_tween_data:
                            obj.tweendata = None
                parentsurface = obj.parentsurface
                obj.absx = int(parentsurface.absx + parentsurface.abswidth * obj.scalex + obj.x)
                obj.absy = int(parentsurface.absy + parentsurface.absheight * obj.scaley + obj.y)
                obj.abswidth = int(parentsurface.abswidth * obj.scalew + obj.width)
                obj.absheight = int(parentsurface.absheight * obj.scaleh + obj.height)

        userstatistics.UserStatistics.stats.increment("temps_jeu", passed)
        currentstate, statetime = statemanager.StateManager.getstate(), statemanager.StateManager.getstatetime()
        if currentstate == statemanager.StateEnum.INITIALISATION:
            if statetime >= 3000:  # on attends 3 secondes avant de commencer, parce que sinon, la transition de l'intro est moins fluide
                Model.model.intro.start()
        elif currentstate == statemanager.StateEnum.INTRO:
            Model.model.intro.update()
        elif currentstate == statemanager.StateEnum.PLAYING:
            coregame.CoreGame.current_core.loop(passed)

    @classmethod
    def mousebutton1down(cls, position):  # click gauche
        for bouton in list(button.Button.getButtons()):
            bouton.mousein = f.checkmousebouton(position, bouton.absx, bouton.absy, bouton.abswidth, bouton.absheight)
            if bouton.mousein:
                bouton.click()
        for checkboxe in checkbox.Checkbox.getCheckboxes():
            if f.checkmousebouton(position, checkboxe.absx,
                                  checkboxe.absy + int(checkboxe.height / 2 - checkboxe.boxsize / 2), checkboxe.boxsize,
                                  checkboxe.boxsize):  # si on est en train de cliquer dessus
                checkboxe.check()
        for tabb in tab.Tab.getTabs():
            if f.checkmousebouton(position, tabb.absx, tabb.absy, tabb.abswidth, tabb.absheight):
                tabb.select()
        for textboxe in list(textbox.Textbox.getTextboxes()):
            if f.checkmousebouton(position, textboxe.absx, textboxe.absy, textboxe.abswidth, textboxe.absheight):
                textboxe.focus()
            else:
                textboxe.unfocus()

    @classmethod
    def mousebutton1up(cls):
        for bouton in list(button.Button.getButtons()):
            if bouton.mousein and bouton.clicking:
                bouton.unclick()

    @classmethod
    def mousebutton1move(cls, position):
        for bouton in list(button.Button.getButtons()):
            bouton.mousein = f.checkmousebouton(position, bouton.absx, bouton.absy, bouton.abswidth, bouton.absheight)

    @classmethod
    def keydown(cls, event):
        if statemanager.StateManager.getstate() == statemanager.StateEnum.PLAYING:
            coregame.CoreGame.keypressed(event)
        else:
            char = event.dict["unicode"]
            if char != "":
                for textboxe in list(textbox.Textbox.getTextboxes()):
                    if textboxe.focused:
                        textboxe.addchar(char)

    @classmethod
    def main_menu(cls, from_return=False):

        if not from_return:  # la fuite de mémoire était causé par le fait qu'on faisait un nouvel objet image en cliquant sur retour...
            # creation de l'image d'arrière plan du menu
            REPERTOIRE = "assets/img/background_temporaire.png"
            POSITION_X = 0
            POSITION_Y = 0
            SCALE_X = 0
            SCALE_Y = 0
            LARGEUR = 0
            HAUTEUR = 0
            SCALE_WIDTH = 1
            SCALE_HEIGHT = 1
            COULEUR = constantes.WHITE
            BORDURE = 0

            image.Image(REPERTOIRE, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                        HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        self = Model.model

        if self.update_reminded or not f.can_update(self.version, self.latest_version):
            # La surface où on va mettre les boutons (pour les positionner plus facilement par la suite)
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
            ALPHA = 255  # opaque...
            CONVERT_ALPHA = True  # ...mais transparent

            surface_boutons = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X,
                                              SCALE_Y, LARGEUR,
                                              HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

            POSITION_X = 0
            POSITION_Y = 0
            SCALE_X = 0
            SCALE_Y = 0
            LARGEUR = 0
            HAUTEUR = 50
            SCALE_WIDTH = 1
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

            button.BJouer(f.translate("play"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                          CENTRE_X, CENTRE_Y,
                          ECART, surface_boutons, POSITION_X, POSITION_Y, SCALE_X,
                          SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
            POSITION_Y += 75
            button.BStats(f.translate("statistics"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                          CENTRE_X,
                          CENTRE_Y,
                          ECART, surface_boutons, POSITION_X, POSITION_Y, SCALE_X,
                          SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
            POSITION_Y += 75
            button.BParam(f.translate("settings"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                          CENTRE_X, CENTRE_Y,
                          ECART, surface_boutons, POSITION_X, POSITION_Y, SCALE_X,
                          SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

            ANTIALIAS = True
            COULEUR = constantes.BLACK  # couleur du texte
            FONT = "Arial"
            TAILLE_FONT = 22
            CENTRE_X = True  # centré sur l'axe x
            CENTRE_Y = True  # centré sur l'axe y
            ARRIERE_PLAN = None
            ECART = 0
            SEUL = True
            LARGEUR = 60
            HAUTEUR = 30
            POSITION_X = - LARGEUR
            POSITION_Y = - HAUTEUR
            SCALE_X = 1
            SCALE_Y = 1
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = constantes.WHITE
            BORDURE = 0

            text.Text("V" + self.version, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                      ECART,
                      SEUL, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                      HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)
        else:
            self.update_reminded = True

            LARGEUR = 500
            HAUTEUR = 200
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

            surface_update = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X,
                                             SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

            ANTIALIAS = True
            COULEUR = constantes.BLACK
            FONT = "Arial"
            TAILLE_FONT = 35
            CENTRE_X = True
            CENTRE_Y = True
            ARRIERE_PLAN = None
            ECART = 0
            SEUL = True
            LARGEUR = 480
            HAUTEUR = 50
            POSITION_X = 10
            POSITION_Y = 10
            SCALE_X = 0
            SCALE_Y = 0
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = constantes.WHITE
            BORDURE = 0

            text.Text(f.translate("update"), ANTIALIAS, COULEUR, FONT, TAILLE_FONT,
                      CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART, SEUL, surface_update, POSITION_X, POSITION_Y, SCALE_X,
                      SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

            HAUTEUR = 30
            TAILLE_FONT = 22
            POSITION_Y += 75

            text.Text(f.translate("update_1") + " (V" + self.latest_version + ").", ANTIALIAS, COULEUR, FONT,
                      TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,
                      SEUL, surface_update, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR,
                      SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)
            POSITION_Y += 25
            text.Text(f.translate("update_2"), ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                      ECART,
                      SEUL, surface_update, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR,
                      SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

            POSITION_X = 20
            POSITION_Y = 150
            SCALE_X = 0
            SCALE_Y = 0
            LARGEUR = 140
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

            button.BYesUpdate(f.translate("yes"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                              CENTRE_X, CENTRE_Y,
                              ECART, surface_update, POSITION_X, POSITION_Y, SCALE_X,
                              SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
            POSITION_X += LARGEUR + 20
            button.BLaterUpdate(f.translate("later"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                                CENTRE_X, CENTRE_Y,
                                ECART, surface_update, POSITION_X, POSITION_Y, SCALE_X,
                                SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
            POSITION_X += LARGEUR + 20
            button.BNoUpdate(f.translate("no"), ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT,
                             CENTRE_X, CENTRE_Y,
                             ECART, surface_update, POSITION_X, POSITION_Y, SCALE_X,
                             SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
