import functions as f
import constantes
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

        image_menu = self.pygame.image.load(f.resource_path("assets/img/menu_fond.png")).convert_alpha()
        self.pygame.display.set_icon(image_menu)  # Icone du jeu
        View.pygame = pygame

    def updatewindow(cls, newsize):  # quand la fenêtre est redimensionnée, ou initialisée
        old_screen_obj = View.screen

        View.screensize = newsize
        screen = uielement.UIelement(None, 0, 0, 0, 0, newsize[0], newsize[1], 0, 0, constantes.WHITE, 0, "screen",
                                     None, True)
        screen.referance = View.pygame.display.set_mode(newsize, View.pygame.RESIZABLE)
        View.screen = screen

        UIelements = uielement.UIelement.getUIelements()
        for classname in UIelements:
            for obj in UIelements[classname]:
                if obj.parentsurface == old_screen_obj:  # tous les objets qui ont pour référence l'ancien objet écran sont mis à jour
                    screen.addchild(obj)

    def checktween(self):
        tweendata = self.tweendata
        advanceratio = tweendata["passed"] / tweendata["duration"]

        for attributdict in tweendata["attributes"]:
            attrname = attributdict["attrname"]
            self.__setattr__(attrname, int(attributdict[attrname + " start"] + attributdict["delta " + attrname] * advanceratio))

    def updatescreen(cls, passed):
        a = View.pygame.Surface(View.screensize)  # une surface pour reset l'écran
        a.fill((255, 255, 255))
        View.screen.referance.blit(a, (0, 0))

        UIelements = uielement.UIelement.getUIelements()
        tweenobj = []

        for classname in UIelements:  # on met à jour les position absolues des éléments graphiques en premier...
            for obj in UIelements[classname]:
                if hasattr(obj, "tweendata") and obj.tweendata:  # tout d'abord, on calcule la nouvelle valeur des attributs qui sont transitionnés
                    View.checktween(obj)
                    tweenobj.append(obj)
                parentsurface = obj.parentsurface
                obj.absx = int(parentsurface.absx + parentsurface.abswidth * obj.scalex + obj.x)
                obj.absy = int(parentsurface.absy + parentsurface.absheight * obj.scaley + obj.y)
                obj.abswidth = int(parentsurface.abswidth * obj.scalew + obj.width)
                obj.absheight = int(parentsurface.absheight * obj.scaleh + obj.height)

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
                            int(obj.parentsurface.abswidth * obj.scalex + obj.x + textobj.x),
                            int(obj.parentsurface.absheight * obj.scaley + obj.y + textobj.y)))
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
                            int(obj.parentsurface.abswidth * obj.scalex + obj.x),
                            int(obj.parentsurface.absheight * obj.scaley + obj.y)))

        if "Surface" in UIelements:
            for surface in UIelements["Surface"]:
                surface.parentsurface.referance.blit(surface.referance, (
                surface.parentsurface.abswidth * surface.scalex + surface.x, surface.parentsurface.absheight * surface.scaley + surface.y))

        # Dessine le personnage en dernier (si le jeu n'est pas fini)
        if not coregame.CoreGame.finished:
            characters = coregame.CoreGame.getCharacterSprites()

            for character in characters:
                character.absx = int(View.screen.abswidth * character.scalex + character.x)
                character.absy = int(View.screen.absheight * character.scaley + character.y)
                attrname = character.state + "sprite"
                state_sprite = character.__getattribute__(attrname)
                View.screen.referance.blit(state_sprite.strip[state_sprite.compteur], (state_sprite.absx + state_sprite.offsetx, state_sprite.absy + state_sprite.offsety))  # On suppose pour l'instant qu'on ne va dessiner les sprites que sur la surface de l'écran

        View.pygame.display.update()

        for obj in tweenobj:
            obj.tweendata["passed"] += passed / 1000
            if obj.tweendata["passed"] >= obj.tweendata["duration"]:
                obj.tweendata["passed"] = obj.tweendata["duration"]
                View.checktween(obj)  # on met la durée à l'état final, car il peut y avoir de gros décalage en cas de performance pas assez élevé
                delattr(obj, "tweendata")  # transition finie

    updatewindow = classmethod(updatewindow)
    updatescreen = classmethod(updatescreen)
