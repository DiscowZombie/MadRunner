import view
import controller
import constantes
import statemanager


class Model:
    pygame = None
    screen = None

    introplaying = False
    introfinished = False
    firstintro = False  # première phase de l'intro: montrer l'icône et le nom
    secondintro = False  # deuxième phase de l'intro: effet de transiton
    objetsintro = []  # tous les objets de l'intro

    def __init__(self, pygame):
        Model.pygame = pygame

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

        surface_intro = Surface(ALPHA, CONVERT_ALPHA, Model.screen, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
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

        image_intro = Image(REPERTOIRE, surface_intro.referance, (surface_intro.x, surface_intro.y), POSITION_X,
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

        texte_intro = Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,
                           surface_intro.referance, (surface_intro.x, surface_intro.y), POSITION_X, POSITION_Y, LARGEUR,
                           HAUTEUR, COULEUR_ARRIERE, BORDURE)

        Model.objetsintro.append(surface_intro)
        Model.objetsintro.append(image_intro)
        Model.objetsintro.append(texte_intro)

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
        return hasattr(Surface.getSurfaces()[0], "tweendata")

    def middleintro(cls):
        Model.firstintro = False
        Model.secondintro = True
        surfaceintro = Surface.getSurfaces()[0]
        surfaceintro.tween(surfaceintro.x, surfaceintro.y, surfaceintro.width, surfaceintro.height, 1, {
            "name": "alpha",
            "value": 0  # transparent
        })

    def endintro(cls):
        statemanager.StateManager.setstate(statemanager.StateEnum.MAIN_MENU)
        Model.secondintro = False
        Model.introplaying = False
        for objet in Model.objetsintro:
            del objet
        del Model.objetsintro

        Model.main_menu()

    objetsmenu = []

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

        image_menu = Image(REPERTOIRE, Model.screen, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR, HAUTEUR,
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

        surface_boutons = Surface(ALPHA, CONVERT_ALPHA, Model.screen, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
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

        bouton_jouer = BJouer("Jouer", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                              ECART, surface_boutons.referance, POSITION_SURFACE, POSITION_X, POSITION_Y, LARGEUR,
                              HAUTEUR, COULEUR, BORDURE)
        POSITION_Y += 75
        bouton_stats = BStats("Statistiques", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                              ARRIERE_PLAN, ECART, surface_boutons.referance, POSITION_SURFACE, POSITION_X, POSITION_Y,
                              LARGEUR, HAUTEUR, COULEUR, BORDURE)
        POSITION_Y += 75
        bouton_param = BParam("Paramètres", ANTIALIAS, COULEUR_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                              ARRIERE_PLAN, ECART, surface_boutons.referance, POSITION_SURFACE, POSITION_X, POSITION_Y,
                              LARGEUR, HAUTEUR, COULEUR, BORDURE)

        Model.objetsmenu.append(image_menu)
        Model.objetsmenu.append(surface_boutons)
        Model.objetsmenu.append(bouton_jouer)
        Model.objetsmenu.append(bouton_stats)
        Model.objetsmenu.append(bouton_param)

    initscreen = classmethod(initscreen)
    startintro = classmethod(startintro)
    introsurfacetweening = classmethod(introsurfacetweening)
    middleintro = classmethod(middleintro)
    endintro = classmethod(endintro)

    main_menu = classmethod(main_menu)


""""""""""""""""""""""""""""""""""""
""" GERE LES ELEMENTS GRAPHIQUES """
""""""""""""""""""""""""""""""""""""


class UIelement:
    UIelements = {}

    """
    :param surface_bouton - La surface où sera l'élément graphique
    :param surface_position - La position de la surface où on va mettre l'élément graphique
    :param posx - La position x de l'élément graphique
    :param posy - La position y de l'élément graphique
    :param width - La largeur de l'élément graphique
    :param height - La hauteur de l'élément graphique
    :param color - La couleur d'arrière plan de l'élément graphique
    :param bordersize - Le taille de la bordure en pixel de l'élément graphique (s'il vaut 0, l'élément est repli)
    """

    def __init__(self, surface_bouton, surface_position, posx, posy, width, height, color, bordersize, classname,
                 alpha=None):
        self.x = posx
        self.y = posy
        self.absx = surface_position[
                        0] + posx  # position "absolue", càd, position par rapport à la fenêtre, et non la surface où on dessine l'élément
        self.absy = surface_position[1] + posy
        self.width = width
        self.height = height
        self.color = color
        self.bordersize = bordersize
        self.alpha = alpha
        self.classname = classname  # pas sûr que ce sera utile
        self.ismousein = False
        self.tweendata = None
        self.parentsurface = surface_bouton

        if not classname in UIelement.UIelements:
            UIelement.UIelements[classname] = []  # on l'ajoute aux éléments UI, en les triant par leur "classname"

        UIelement.UIelements[classname].append(self)

    def tween(self, posx, posy, width, height, duration,
              *otherattr):  # transition linéaire de la position et/ou de la taille, "duration" en secondes, on peut éventuellement fare une transition d'autres attributs
        self.tweendata = {
            "delta x": posx - self.x,
            "delta y": posy - self.y,
            "delta width": width - self.width,
            "delta height": height - self.height,
            "x start": self.x,
            "y start": self.y,
            "width start": self.width,
            "height start": self.height,
            "duration": duration,
            "passed": 0
        }

        if otherattr:  # pour ajouter des autres attricuts à transitionner, mettre dans dans une liste un dictionnaire avec son nom ["name"] et sa valeur ["value"]
            if not "otherattr" in self.tweendata:
                self.tweendata["otherattr"] = []

            for attributdict in otherattr:
                attrname = attributdict["name"]
                attrvalue = attributdict["value"]
                currentattrvalue = self.__getattribute__(attrname)

                tweendict = {
                    "attrname": attrname,
                    "delta " + attrname: attrvalue - currentattrvalue,
                    attrname + " start": currentattrvalue
                }

                self.tweendata["otherattr"].append(tweendict)

    def getUIelements(cls):
        return UIelement.UIelements

    getUIelements = classmethod(getUIelements)


class Surface(UIelement):
    surfaces = []

    def __init__(self, alpha=None, convert_alpha=False, *UIargs):
        UIelement.__init__(self, *UIargs, "Surface", alpha)

        self.convertalpha = convert_alpha
        self.referance = view.View.createsurface(self)

        Surface.surfaces.append(self)

    def getSurfaces(cls):
        return Surface.surfaces

    getSurfaces = classmethod(getSurfaces)


class Image(UIelement):
    images = []

    """
    :param image_path - Le chemin vers l'image
    :param *UIargs - Tous les paramètres d'un élément graphique (voir classe "UIelement")
    """

    def __init__(self, image_path, *UIargs):
        UIelement.__init__(self, *UIargs, "Image")

        self.imagepath = image_path
        self.originalimage = view.View.createimage(self, False)
        self.referance = view.View.createimage(self,
                                               True)  # on creer l'image pour avoir une référence vers celui-ci, mais sans nécessairement l'afficher

        Image.images.append(self)

    def getImages(cls):
        return Image.images

    getImages = classmethod(getImages)


class Text(UIelement):
    texts = []

    def __init__(self, text, antialias, couleur_text, font, font_size, centeredx, centeredy, backgroundcolor, offset,
                 *UIargs):
        UIelement.__init__(self, *UIargs, "Text")

        self.text = text
        self.antialias = antialias
        self.textcolor = couleur_text
        self.font = font
        self.fontsize = font_size
        self.textcenteredx = centeredx
        self.textcenteredy = centeredy
        self.backgroundcolor = backgroundcolor
        self.textoffset = offset
        view.View.createtext(self)  # self.referance va être attribué en appelant cette fonction

        Text.texts.append(self)

    def getTexts(cls):
        return Text.texts

    getTexts = classmethod(getTexts)


class Button(UIelement):
    boutons = []

    """
    :param text - Le texte sur le bouton
    :param couleur_text - La couleur du texte
    :param font - Le font du texte
    :param font_size - La taille du font
    :param centeredx - Le texte est-il centré sur l'axe x ?
    :param centeredy - Le texte est-il centré sur l'axe y ?
    :param offset - Le nombre de pixel de décalage du texte sur l'axe x
    :param *UIargs - Tous les paramètres d'un élément graphique (voir classe "UIelement")
    """

    def __init__(self, text, antialias, couleur_text, font, font_size, centeredx, centeredy, backgroundcolor, offset,
                 *UIargs):

        UIelement.__init__(self, *UIargs, "Button")

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
        view.View.createbutton(self)
        """
        ATTENTION: CETTE OBJET N'A PAS DE REFERENCE, MAIS A UNE REFERENCE VERS LA SURFACE DU TEXTE AVEC L'ATTRIBUT "textsurface"
        """
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

    def __del__(self):
        if self in Button.boutons:
            Button.boutons.remove(self)  # on l'enlève de nos tables de boutons avant de le détruire
        del self

    def getButtons(cls):
        return Button.boutons

    getButtons = classmethod(getButtons)


class BJouer(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(
            self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        view.View.drawmenu()  # on dessine le menu par dessus

        POSITION_SURFACE = (120, 165)
        TAILLE_SURFACE = [400, 150]
        surfacetrans = Model.pygame.Surface(TAILLE_SURFACE, Model.pygame.SRCALPHA,
                                            32)  # La surface où on va mettre les boutons (pour les positionner plus facilement par la suite)
        surfacetrans = surfacetrans.convert_alpha()  # Il faut cependant que la surface a un arrière plan transparent

        POSX = 0
        POSY = 0
        WIDTH = 400
        HEIGHT = 50

        B1Joueur(Model.pygame, "1 joueur", surfacetrans, POSITION_SURFACE, POSX, POSY, WIDTH, HEIGHT, constantes.GRAY,
                 0,
                 constantes.BLACK, "Arial", 24, True, True, 0)
        POSY += 75
        B2Joueurs(Model.pygame, "2 joueurs", surfacetrans, POSITION_SURFACE, POSX, POSY, WIDTH, HEIGHT, constantes.GRAY,
                  0,
                  constantes.BLACK, "Arial", 24, True, True, 0)

        view.View.drawreturn()

        view.View.screen.blit(surfacetrans, POSITION_SURFACE)

        # pygame.display.update()


class BParam(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(
            self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        pass


class BStats(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(
            self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        pass


class B1Joueur(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(
            self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        pass


class B2Joueurs(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(
            self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        pass


class BRetour(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(
            self):  # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        view.View.drawmenu()
        view.View.drawmainmenu()
