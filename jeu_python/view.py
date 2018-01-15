import time
import toolbox
import functions as f
import constantes
import statemanager


class View:
    pygame = None
    screen = None

    def __init__(self, pygame):
        screen = pygame.display.set_mode((640, 480))  # fenêtre de 640 sur 480
        screen.fill((255, 255, 255))
        pygame.display.set_caption("Mad Runner")

        image_menu = pygame.image.load("assets/img/menu_fond.png").convert_alpha()
        pygame.display.set_icon(image_menu)  # Icone du jeu

        View.pygame = pygame
        View.screen = screen

        toolbox.Model.initscreen(screen)

    def mousebutton1down(self, position):  # click gauche
        boutons = toolbox.Button.getButtons()
        for bouton in boutons:
            bouton.mousein = f.checkmousebouton(position, bouton.x, bouton.y, bouton.width, bouton.height)

    def mousebutton1up(self, position):
        print("plus en train de click")

    def drawreturn(cls):
        POSITION_BOUTON = (0, 0)
        TAILLE_BOUTON = [100, 50]
        surfacetrans = View.pygame.Surface(TAILLE_BOUTON, View.pygame.SRCALPHA,
                                           32)  # La surface où on va mettre les boutons (pour les positionner plus facilement par la suite)
        surfacetrans = surfacetrans.convert_alpha()  # Il faut cependant que la surface a un arrière plan transparent

        toolbox.BRetour(View.pygame, "Retour", surfacetrans, POSITION_BOUTON, POSITION_BOUTON[0], POSITION_BOUTON[1],
                        TAILLE_BOUTON[0], TAILLE_BOUTON[1], constantes.GRAY, 0,
                        constantes.BLACK, "Arial", 24, True, True, 0)

        View.screen.blit(surfacetrans, POSITION_BOUTON)

    def createimage(self, resize):
        image = View.pygame.image.load(self.imagepath).convert_alpha()
        if resize:
            image = View.pygame.transform.scale(image, (self.width, self.height))
        return image

    def drawimage(self):
        self.referance = View.pygame.transform.scale(self.originalimage, (self.width, self.height))

    def createsurface(self):
        if self.convertalpha:
            return View.pygame.Surface((self.width, self.height), View.pygame.SRCALPHA, 32)
        else:
            return View.pygame.Surface((self.width, self.height))

    def drawsurface(self):
        surface = self.referance
        if self.convertalpha:
            surface.convert_alpha(self.referance)
        else:
            surface.fill(self.color)
            surface.set_alpha(self.alpha)

    def createtext(self):
        texte = View.pygame.font.SysFont(self.font, self.fontsize)
        surfacetext = texte.render(self.text, self.antialias, self.textcolor,
                                   self.backgroundcolor)  # retourne la surface sur laquelle le texte est dessiné
        self.textreferance = texte
        self.referance = surfacetext

    def createbutton(self):
        View.pygame.draw.rect(self.parentsurface, self.color, [self.x, self.y, self.width, self.height],
                              self.bordersize)
        View.createtext(self)

    def drawbutton(self):
        View.createbutton(self)
        if self.textcenteredx or self.textcenteredy:
            positionx, positiony = f.centretexte(self.textreferance.size(self.text), (self.width, self.height))
            if not self.textcenteredx:
                positionx = 0
            if not self.textcenteredy:
                positiony = 0
        else:
            positionx, positiony = 0, 0

        self.parentsurface.blit(self.referance, (positionx + self.textoffset, self.y + positiony))
        del self.referance

    def checktween(self):
        tweendata = self.tweendata
        advanceratio = tweendata["passed"] / tweendata["duration"]
        self.x = int(tweendata["x start"] + tweendata["delta x"] * advanceratio)
        self.y = int(tweendata["y start"] + tweendata["delta y"] * advanceratio)
        self.width = int(tweendata["width start"] + tweendata["delta width"] * advanceratio)
        self.height = int(tweendata["height start"] + tweendata["delta height"] * advanceratio)

        if "otherattr" in tweendata:
            for attributdict in tweendata["otherattr"]:
                attrname = attributdict["attrname"]
                self.__setattr__(attrname, int(
                    attributdict[attrname + " start"] + attributdict["delta " + attrname] * advanceratio))

    def updatescreen(cls, passed):

        a = View.pygame.Surface((640, 480))  # une surface pour reset l'écran
        a.fill((255, 255, 255))
        View.screen.blit(a, (0, 0))

        currentstate, statetime = statemanager.StateManager.getstate(), statemanager.StateManager.getstatetime()
        if currentstate == statemanager.StateEnum.INITIALISATION:
            if statetime >= 3000:  # on attends 3 secondes avant de commencer, parce que sinon, la transition de l'intro est moins fluide
                toolbox.Model.startintro()
        elif currentstate == statemanager.StateEnum.INTRO:
            if not toolbox.Model.introsurfacetweening():  # si on est en train d'attendre
                statemanager.StateManager.referancetimer += passed
                referancetime = statemanager.StateManager.referancetimer
                if toolbox.Model.firstintro and referancetime >= 2000:
                    toolbox.Model.middleintro()
                elif toolbox.Model.secondintro and referancetime >= 2000:
                    toolbox.Model.endintro()
        elif currentstate == statemanager.StateEnum.MAIN_MENU:
            pass

        UIelements = toolbox.UIelement.getUIelements()
        tweenobj = []

        if "Surface" in UIelements:
            for surface in UIelements["Surface"]:  # on met à jour les surfaces en premier !
                View.drawsurface(surface)
        for classname in UIelements:
            for obj in UIelements[classname]:
                if hasattr(obj, "tweendata") and obj.tweendata:
                    View.checktween(obj)
                    tweenobj.append(obj)
            if classname != "Surface":
                functiontorun = None
                if classname == "Image":
                    functiontorun = View.drawimage
                elif classname == "Text":
                    functiontorun = View.createtext
                elif classname == "Button":
                    functiontorun = View.drawbutton

                for obj in UIelements[classname]:
                    functiontorun(obj)

                    if hasattr(obj, "referance"):
                        if type(obj.referance) is dict:
                            for referancename in obj.referance:
                                obj.parentsurface.blit(obj.referance[referancename], (obj.x, obj.y))
                        else:
                            obj.parentsurface.blit(obj.referance, (obj.x, obj.y))

        for surface in toolbox.Surface.getSurfaces():
            View.screen.blit(surface.referance, (surface.x, surface.y))

        View.pygame.display.update()

        for obj in tweenobj:
            obj.tweendata["passed"] += passed / 1000
            if obj.tweendata["passed"] >= obj.tweendata["duration"]:
                obj.tweendata["passed"] = obj.tweendata["duration"]
                View.checktween(
                    obj)  # on met la durée à l'état final, car il peut y avoir de gros décalage en cas de performance pas assez élevé
                del obj.tweendata  # transition finie

    drawreturn = classmethod(drawreturn)
    updatescreen = classmethod(updatescreen)

    """"
    @staticmethod
    def createbouton(pygame, name, surface_bouton, surface_position, posx, posy, width, height, couleur_bouton,
                     bordersize, couleur_text, font, font_size, centeredx, centeredy, offset):
        pygame.draw.rect(surface_bouton, couleur_bouton, [posx, posy, width, height], bordersize)
        texte = pygame.font.SysFont(font, font_size)
        if centeredx or centeredy:
            positionx, positiony = f.centretexte(texte.size(name), (width, height))
            if not centeredx:
                positionx = 0
            if not centeredy:
                positiony = 0
        else:
            positionx, positiony = 0, 0

        surface_bouton.blit(texte.render(str(name), True, couleur_text), (positionx + offset, posy + positiony))
    """
