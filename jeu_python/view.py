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

        image_menu = self.pygame.image.load(f.resource_path("assets\img\menu_fond.png")).convert_alpha()
        self.pygame.display.set_icon(image_menu)  # Icône du jeu
        View.pygame = pygame

    def updatewindow(cls, newsize):  # quand la fenêtre est redimensionnée, ou initialisée
        old_screen_obj = View.screen

        View.screensize = newsize
        screen = uielement.UIelement(None, 0, 0, 0, 0, newsize[0], newsize[1], 0, 0, constantes.WHITE, 0, "screen",
                                     None, True)
        screen.referance = View.pygame.display.set_mode(newsize, View.pygame.RESIZABLE)
        View.screen = screen
        View.screen.updated = True  # n'est sur True que pendant 1 image ! Il permet aux objets de savoir que l'écran a été redimensionné

        UIelements = uielement.UIelement.getUIelements()
        for classname in UIelements:
            for obj in UIelements[classname]:
                if obj.parentsurface == old_screen_obj:  # tous les objets qui ont pour référence l'ancien objet écran sont mis à jour
                    screen.addchild(obj)

    def updatescreen(cls):
        a = View.pygame.Surface(View.screensize)  # une surface pour reset l'écran
        a.fill((255, 255, 255))
        View.screen.referance.blit(a, (0, 0))

        UIelements = uielement.UIelement.getUIelements()

        if "Surface" in UIelements:
            for surface in UIelements["Surface"]:  # ...puis on met à jour les surfaces...
                surface.draw()
        if "Rect" in UIelements:
            for rect in UIelements["Rect"]:  # ...puis les rectangles contenues dans les surfaces...
                if rect.visible:
                    rect.draw()
        for classname in UIelements:  # ...puis le reste...
            if classname != "Surface" and classname != "Rect":
                for obj in UIelements[classname]:
                    obj.draw()
                    if hasattr(obj, "referance") and obj.visible:
                        if classname == "Button":  # exception pour les boutons qui ne vont pas être blité comme les autres...
                            textobj = obj.textobj
                            obj.parentsurface.referance.blit(textobj.referance, (
                            int(obj.parentsurface.abswidth * obj.scalex + obj.x + textobj.x),
                            int(obj.parentsurface.absheight * obj.scaley + obj.y + textobj.y)))
                        elif classname == "Checkbox":  # ... et les checkbox aussi...
                            textobj = obj.textobj
                            obj.parentsurface.referance.blit(textobj.referance, (
                            int(obj.parentsurface.abswidth * obj.scalex + obj.x + textobj.x + obj.boxsize),
                            int(obj.parentsurface.absheight * obj.scaley + obj.y + textobj.y)))
                            if obj.checked:
                                obj.parentsurface.referance.blit(obj.checkreferance, (
                                int(obj.parentsurface.abswidth * obj.scalex + obj.x + obj.x),
                                int(obj.parentsurface.absheight * obj.scaley + obj.y) + int(
                                    obj.height / 2 - obj.boxsize / 2)))
                        elif classname == "Tab":  # ... et les tabs aussi...
                            textobj = obj.textobj
                            obj.parentsurface.referance.blit(textobj.referance, (
                            int(obj.parentsurface.abswidth * obj.scalex + obj.x + textobj.x),
                            int(obj.parentsurface.absheight * obj.scaley + obj.y + textobj.y)))
                            if obj.imagereferance:
                                obj.parentsurface.referance.blit(obj.imagereferance, (obj.x + 10, obj.y + 5))
                        elif classname == "Textbox":  # ... et les textbox aussi
                            textobj = obj.textobj
                            obj.parentsurface.referance.blit(textobj.referance, (
                            int(obj.parentsurface.abswidth * obj.scalex + obj.x + textobj.x),
                            int(obj.parentsurface.absheight * obj.scaley + obj.y + textobj.y)))
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
                if surface.visible:
                    surface.parentsurface.referance.blit(surface.referance, (
                    surface.parentsurface.abswidth * surface.scalex + surface.x, surface.parentsurface.absheight * surface.scaley + surface.y))

        # Dessine le personnage en dernier (si le jeu n'est pas fini)
        if statemanager.StateManager.getstate() == statemanager.StateEnum.PLAYING and not coregame.CoreGame.current_core.finished:
            for character in coregame.Character.getCharacters():
                character.absx = int(View.screen.abswidth * character.scalex + character.x)
                character.absy = int(View.screen.absheight * character.scaley + character.y)
                attrname = character.state + "sprite"
                state_sprite = character.__getattribute__(attrname)
                View.screen.referance.blit(state_sprite.strip[state_sprite.compteur], (character.absx + state_sprite.x, character.absy + state_sprite.y))  # On suppose pour l'instant qu'on ne va dessiner les sprites que sur la surface de l'écran

        View.pygame.display.update()
        View.screen.updated = False

    updatewindow = classmethod(updatewindow)
    updatescreen = classmethod(updatescreen)
