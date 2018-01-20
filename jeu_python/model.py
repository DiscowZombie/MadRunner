import view
import controller
import constantes
import statemanager
import functions as f

import uielements.text as text
import uielements.surface as surface
import uielements.button as button
import uielements.image as image
import uielements.checkbox as checkbox

class Model:
    pygame = None
    screen = None

    introplaying = False
    introfinished = False
    firstintro = False  # première phase de l'intro: montrer l'icône et le nom
    secondintro = False  # deuxième phase de l'intro: effet de transiton
    tempobjets = []  # une liste d'objets temporaires

    def __init__(self, pygame):
        Model.pygame = pygame

    def mousebutton1down(cls, position):  # click gauche
        for bouton in list(button.Button.getButtons()):
            bouton.mousein = f.checkmousebouton(position, bouton.absx, bouton.absy, bouton.width, bouton.height)
        for checkboxe in checkbox.Checkbox.getCheckboxes():
            if f.checkmousebouton(position, checkboxe.absx, checkboxe.absy + int(checkboxe.height/2 - checkboxe.boxsize/2), checkboxe.boxsize, checkboxe.boxsize):  # si on est en train de cliquer dessus
                checkboxe.check()

    def mousebutton1up(cls, position):
        print("plus en train de click")

    def initscreen(cls, screen):
        Model.screen = screen

    def startintro(cls):
        statemanager.StateManager.setstate(statemanager.StateEnum.INTRO)
        Model.introplaying = True
        Model.firstintro = True

        # état initial de la surface où on va mettre le logo et le titire du jeu
        POSITION_SURFACE = (0, 0)
        POSITION_X = 220
        POSITION_Y = 120
        LARGEUR = 225
        HAUTEUR = 225
        COULEUR = constantes.WHITE
        BORDURE = 0  # rempli
        ALPHA = 0  # transarence
        CONVERT_ALPHA = False

        surface_intro = surface.Surface(ALPHA, CONVERT_ALPHA, Model.screen, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
                                HAUTEUR, COULEUR,
                                BORDURE)  # creation de la l'objet surface où on va mettre le titire et l'image du jeu

        # état intial de l'image du logo
        REPERTOIRE = "assets/img/menu_fond.png"
        POSITION_X = 100
        POSITION_Y = 140
        LARGEUR = 0
        HAUTEUR = 0
        COULEUR = constantes.WHITE
        BORDURE = 0

        image_intro = image.Image(REPERTOIRE, surface_intro.referance, (surface_intro.x, surface_intro.y), POSITION_X,
                            POSITION_Y, LARGEUR, HAUTEUR, COULEUR, BORDURE)

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
        POSITION_X = 100
        POSITION_Y = 0
        LARGEUR = 0
        HAUTEUR = 0
        COULEUR_ARRIERE = constantes.WHITE
        BORDURE = 0

        texte_intro = text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,
                           surface_intro.referance, (surface_intro.x, surface_intro.y), POSITION_X, POSITION_Y, LARGEUR,
                           HAUTEUR, COULEUR_ARRIERE, BORDURE)

        Model.tempobjets.append(surface_intro)
        Model.tempobjets.append(image_intro)
        Model.tempobjets.append(texte_intro)

        # et enfin, on fait une merveilleuse transition vers l'état final de l'image et du texte
        surface_intro.tween(surface_intro.x, surface_intro.y, surface_intro.width, surface_intro.height, 1, {
            "name": "alpha",
            "value": 255
        })
        image_intro.tween(0, 80, 200, 120, 1)  # posx final, posy final, largeur finale, hauteur finale, durée
        texte_intro.tween(0, 0, 200, 80, 1, {  # transition de la taille du font également
            "name": "fontsize",
            "value": 44
        })

    def introsurfacetweening(cls):
        return hasattr(surface.Surface.getSurfaces()[0], "tweendata")

    def middleintro(cls):
        Model.firstintro = False
        Model.secondintro = True
        surfaceintro = surface.Surface.getSurfaces()[0]
        surfaceintro.tween(surfaceintro.x, surfaceintro.y, surfaceintro.width, surfaceintro.height, 1, {
            "name": "alpha",
            "value": 0  # transparent
        })

    def endintro(cls):
        statemanager.StateManager.setstate(statemanager.StateEnum.MAIN_MENU)
        Model.secondintro = False
        Model.introplaying = False
        for objet in Model.tempobjets:
            objet.__del__() # efface l'objet
        Model.tempobjets.clear()

        Model.main_menu()

    def main_menu(cls):
        # creation de l'image du menu
        REPERTOIRE = "assets/img/background_temporaire.jpg"
        POSITION_SURFACE = (0, 0)
        POSITION_X = 0
        POSITION_Y = 0
        LARGEUR = 640
        HAUTEUR = 480
        COULEUR = constantes.WHITE
        BORDURE = 0

        image_menu = image.Image(REPERTOIRE, Model.screen, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR, HAUTEUR,
                           COULEUR, BORDURE)

        # La surface où on va mettre les boutons (pour les positionner plus facilement par la suite)
        POSITION_SURFACE = (0, 0)
        POSITION_X = 120
        POSITION_Y = 150
        LARGEUR = 400
        HAUTEUR = 200
        COULEUR = constantes.WHITE
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = True

        surface_boutons = surface.Surface(ALPHA, CONVERT_ALPHA, Model.screen, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
                                  HAUTEUR, COULEUR, BORDURE)

        # Les fameux boutons du menu
        POSITION_SURFACE = (120, 150)
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

        button.BJouer("Jouer", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                              ARRIERE_PLAN, ECART, surface_boutons.referance, POSITION_SURFACE, POSITION_X, POSITION_Y,
                              LARGEUR, HAUTEUR, COULEUR, BORDURE)
        POSITION_Y += 75
        button.BStats("Statistiques", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                              ARRIERE_PLAN, ECART, surface_boutons.referance, POSITION_SURFACE, POSITION_X, POSITION_Y,
                              LARGEUR, HAUTEUR, COULEUR, BORDURE)
        POSITION_Y += 75
        button.BParam("Paramètres", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                              ARRIERE_PLAN, ECART, surface_boutons.referance, POSITION_SURFACE, POSITION_X, POSITION_Y,
                              LARGEUR, HAUTEUR, COULEUR, BORDURE)

    initscreen = classmethod(initscreen)
    mousebutton1down = classmethod(mousebutton1down)
    mousebutton1up = classmethod(mousebutton1up)
    startintro = classmethod(startintro)
    introsurfacetweening = classmethod(introsurfacetweening)
    middleintro = classmethod(middleintro)
    endintro = classmethod(endintro)

    main_menu = classmethod(main_menu)
