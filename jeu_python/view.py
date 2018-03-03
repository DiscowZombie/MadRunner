import model
import functions as f
import constantes
import statemanager
import coregame.coregame as coregame

import uielement


class View:
    pygame = None
    screen = None
    screensize = (640, 480)  # taille par défaut de la fenêtre

    def __init__(self, pygame):
        View.pygame = pygame
        self.pygame = pygame
        self.updatewindow(View.screensize)
        self.pygame.display.set_caption("Mad Runner")

        image_menu = self.pygame.image.load("assets/img/menu_fond.png").convert_alpha()
        self.pygame.display.set_icon(image_menu)  # Icone du jeu
        View.pygame = pygame

    def updatewindow(cls, newsize):  # quand la fenêtre est redimensionnée, ou initialisée
        del View.screen  # efface l'ancienne objet écran qui n'est plus utile !
        View.screensize = newsize
        screen = uielement.UIelement(None, 0, 0, 0, 0, newsize[0], newsize[1], 0, 0, constantes.WHITE, 0, "screen",
                                     None, True)
        screen.referance = View.pygame.display.set_mode(newsize, View.pygame.RESIZABLE)
        View.screen = screen

    def checktween(self):
        tweendata = self.tweendata
        advanceratio = tweendata["passed"] / tweendata["duration"]
        self.x = int(tweendata["x start"] + tweendata["delta x"] * advanceratio)
        self.y = int(tweendata["y start"] + tweendata["delta y"] * advanceratio)
        self.scalex = tweendata["scale x start"] + tweendata["delta x scale"] * advanceratio
        self.scaley = tweendata["scale y start"] + tweendata["delta y scale"] * advanceratio
        self.width = int(tweendata["width start"] + tweendata["delta width"] * advanceratio)
        self.height = int(tweendata["height start"] + tweendata["delta height"] * advanceratio)
        self.scalew = tweendata["scale width start"] + tweendata["delta width scale"] * advanceratio
        self.scaleh = tweendata["scale height start"] + tweendata["delta height scale"] * advanceratio

        if "otherattr" in tweendata:
            for attributdict in tweendata["otherattr"]:
                attrname = attributdict["attrname"]
                self.__setattr__(attrname, int(
                    attributdict[attrname + " start"] + attributdict["delta " + attrname] * advanceratio))

    def updatescreen(cls, passed):
        a = View.pygame.Surface(View.screensize)  # une surface pour reset l'écran
        a.fill((255, 255, 255))
        View.screen.referance.blit(a, (0, 0))

        UIelements = uielement.UIelement.getUIelements()
        tweenobj = []

        for classname in UIelements:  # on met à jour les position absolues des éléments graphiques en premier...
            for obj in UIelements[classname]:
                if hasattr(obj,
                           "tweendata") and obj.tweendata:  # tout d'abord, on calcul leur position s'il sont en train de faire une transition
                    View.checktween(obj)
                    tweenobj.append(obj)
                parentsurface = obj.parentsurface
                referance = parentsurface.referance
                obj.absx = int(parentsurface.absx + referance.get_width() * obj.scalex + obj.x)
                obj.absy = int(parentsurface.absy + referance.get_height() * obj.scaley + obj.y)
                obj.abswidth = int(referance.get_width() * obj.scalew + obj.width)
                obj.absheight = int(referance.get_height() * obj.scaleh + obj.height)

        if "Surface" in UIelements:
            for surface in UIelements["Surface"]:  # ...puis on met à jour les surfaces...
                surface.draw()
        if "Rect" in UIelements:
            for rect in UIelements["Rect"]:  # ...puis les rectangles contenues dans les surfaces...
                rect.draw()
        for classname in UIelements:  # ...puis le reste...
            if classname != "Surface" and classname != "Rect":
                for obj in UIelements[classname]:
                    obj.draw()
                    if hasattr(obj, "referance"):
                        if classname == "Button":  # exception pour les boutons qui ne vont pas être blité comme les autres...
                            textobj = obj.textobj
                            obj.parentsurface.referance.blit(textobj.referance, (
                            int(obj.parentsurface.referance.get_width() * obj.scalex + obj.x + textobj.x),
                            int(obj.parentsurface.referance.get_height() * obj.scaley + obj.y + textobj.y)))
                        elif classname == "Checkbox":  # ... et les checkbox aussi
                            textobj = obj.textobj
                            obj.parentsurface.referance.blit(textobj.referance, (
                            int(obj.parentsurface.abswidth * obj.scalex + obj.x + textobj.x + obj.boxsize),
                            int(obj.parentsurface.absheight * obj.scaley + obj.y + textobj.y)))

                            if obj.checked:
                                obj.parentsurface.referance.blit(obj.checkreferance, (
                                int(obj.parentsurface.abswidth * obj.scalex + obj.x + obj.x),
                                int(obj.parentsurface.absheight * obj.scaley + obj.y) + int(
                                    obj.height / 2 - obj.boxsize / 2)))
                        elif classname == "Text":
                            if obj.alone:
                                obj.parentsurface.referance.blit(obj.referance, (
                                int(obj.parentsurface.abswidth * obj.scalex + obj.x),
                                int(obj.parentsurface.absheight * obj.scaley + obj.y)))
                        else:
                            obj.parentsurface.referance.blit(obj.referance, (
                            int(obj.parentsurface.referance.get_width() * obj.scalex + obj.x),
                            int(obj.parentsurface.referance.get_height() * obj.scaley + obj.y)))  # ATTENTION : L'IMAGE NE SE POSITIONNE PAS CORRECTEMENT CAAR LE PARENTSURFACE CONTIENT LES ANCIENNES DIMENSIONS DE L'OBJET ECRAN !

        if "Surface" in UIelements:
            for surface in UIelements["Surface"]:
                parentsize = surface.parentsurface.referance.get_size()
                surface.parentsurface.referance.blit(surface.referance, (
                parentsize[0] * surface.scalex + surface.x, parentsize[1] * surface.scaley + surface.y))

        # on dessine le personnage et les obstacles en dernier
        characters = coregame.CoreGame.characters_sprite

        for character in characters:
            attrname = character.state + "sprite"
            state_sprite = character.__getattribute__(attrname)
            View.screen.referance.blit(state_sprite.strip[state_sprite.compteur], (state_sprite.absx + state_sprite.offsetx, state_sprite.absy + state_sprite.offsety))  #on suppose pour l'instant qu'on ne va dessiner les sprites que sur la surface de l'écran

        View.pygame.display.update()

        for obj in tweenobj:
            obj.tweendata["passed"] += passed / 1000
            if obj.tweendata["passed"] >= obj.tweendata["duration"]:
                obj.tweendata["passed"] = obj.tweendata["duration"]
                View.checktween(obj)  # on met la durée à l'état final, car il peut y avoir de gros décalage en cas de performance pas assez élevé
                delattr(obj, "tweendata")  # transition finie

    updatewindow = classmethod(updatewindow)
    updatescreen = classmethod(updatescreen)
