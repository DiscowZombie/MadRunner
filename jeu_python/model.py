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

from coregame import coregame as coregame

import settings
import json


class Model:
    pygame = None

    introplaying = False
    introfinished = False
    firstintro = False  # première phase de l'intro: montrer l'icône et le nom
    secondintro = False  # deuxième phase de l'intro: effet de transiton

    def __init__(self, pygame):
        Model.pygame = pygame

    def updatemodel(cls, passed):

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
                Model.startintro()
        elif currentstate == statemanager.StateEnum.INTRO:
            if not Model.introsurfacetweening():  # si on est en train d'attendre
                statemanager.StateManager.referancetimer += passed
                referancetime = statemanager.StateManager.referancetimer
                if Model.firstintro and referancetime >= 2000:
                    Model.middleintro()
                elif Model.secondintro and referancetime >= 2500:
                    Model.endintro()
        elif currentstate == statemanager.StateEnum.MAIN_MENU:
            pass
        elif currentstate == statemanager.StateEnum.PLAYING:
            coregame.CoreGame.current_core.loop(passed)

    def mousebutton1down(cls, position):  # click gauche
        for bouton in list(button.Button.getButtons()):
            bouton.mousein = f.checkmousebouton(position, bouton.absx, bouton.absy, bouton.abswidth, bouton.absheight)
        for checkboxe in checkbox.Checkbox.getCheckboxes():
            if f.checkmousebouton(position, checkboxe.absx,
                                  checkboxe.absy + int(checkboxe.height / 2 - checkboxe.boxsize / 2), checkboxe.boxsize,
                                  checkboxe.boxsize):  # si on est en train de cliquer dessus
                checkboxe.check()
        for tabb in tab.Tab.getTabs():
            if f.checkmousebouton(position, tabb.absx, tabb.absy, tabb.abswidth, tabb.absheight):
                tabb.select()

    def mousebutton1up(cls, position):
        print("plus en train de click")

    def startintro(cls):
        statemanager.StateManager.setstate(statemanager.StateEnum.INTRO)
        Model.introplaying = True
        Model.firstintro = True

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
        ALPHA = 0  # transarence
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

        # Charger les statistiques de l'utilisateur et son compte en ligne
        settings.response_json = settings.StatsManager().loadkey()
        if settings.response_json is not None:
            user_id = json.loads(settings.response_json)['id']
            settings.data = settings.CurlManager(constantes.WEBSITE_URI + "statistiques.php?id=" + user_id).readjson()
            
    def introsurfacetweening(cls):
        return surface.Surface.getSurfaces()[0].tweendata

    def middleintro(cls):
        Model.firstintro = False
        Model.secondintro = True
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

    def endintro(cls):
        statemanager.StateManager.setstate(statemanager.StateEnum.MAIN_MENU)
        Model.secondintro = False
        Model.introplaying = False
        surface.Surface.getSurfaces()[0].unreferance()
        Model.main_menu()

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
        ARRIERE_PLAN_TEXTE = COULEUR
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        button.BJouer("Jouer", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                      ARRIERE_PLAN, ECART, surface_boutons, POSITION_X, POSITION_Y, SCALE_X,
                      SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        POSITION_Y += 75
        button.BStats("Statistiques", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X,
                      CENTRE_Y,
                      ARRIERE_PLAN, ECART, surface_boutons, POSITION_X, POSITION_Y, SCALE_X,
                      SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
        POSITION_Y += 75
        button.BParam("Paramètres", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                      ARRIERE_PLAN, ECART, surface_boutons, POSITION_X, POSITION_Y, SCALE_X,
                      SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

    updatemodel = classmethod(updatemodel)
    mousebutton1down = classmethod(mousebutton1down)
    mousebutton1up = classmethod(mousebutton1up)
    startintro = classmethod(startintro)
    introsurfacetweening = classmethod(introsurfacetweening)
    middleintro = classmethod(middleintro)
    endintro = classmethod(endintro)

    main_menu = classmethod(main_menu)
