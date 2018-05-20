import pygame
import uielement


class Surface(uielement.UIelement):
    surfaces = []

    def __init__(self, alpha=None, convert_alpha=False, *UIargs):
        uielement.UIelement.__init__(self, *UIargs, "Surface", alpha)

        self.convertalpha = convert_alpha
        self.referance = self.create()

        Surface.surfaces.append(self)

    def create(self):
        if self.convertalpha:
            surface = pygame.Surface((self.abswidth, self.absheight), pygame.SRCALPHA, 32).convert_alpha()
        else:
            surface = pygame.Surface((self.abswidth, self.absheight)).convert()
            surface.fill(self.color)
            surface.set_alpha(self.alpha)
        return surface

    def draw(self):
        self.referance = self.create()

    def unreferance(self):
        Surface.surfaces.remove(self)
        self.remove()

    @classmethod
    def getSurfaces(cls):
        return Surface.surfaces
