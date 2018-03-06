import uielement
import uielements.rect as rect
import view


class Surface(uielement.UIelement):
    surfaces = []

    def __init__(self, alpha = None, convert_alpha = False, *UIargs):
        uielement.UIelement.__init__(self, *UIargs, "Surface", alpha)

        self.convertalpha = convert_alpha
        self.referance = self.create()

        Surface.surfaces.append(self)

    def create(self):
        if self.convertalpha:
            surface = view.View.pygame.Surface((self.abswidth, self.absheight), view.View.pygame.SRCALPHA, 32)
            surface.convert_alpha(surface)
        else:
            surface = view.View.pygame.Surface((self.abswidth, self.absheight))
            surface.fill(self.color)
            surface.set_alpha(self.alpha)
        return surface

    def draw(self):
        self.referance = self.create()

    def unreferance(self):
        Surface.surfaces.remove(self)
        self.remove()

    def getSurfaces(cls):
        return Surface.surfaces

    getSurfaces = classmethod(getSurfaces)
