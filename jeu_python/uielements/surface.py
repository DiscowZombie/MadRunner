import uielement
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
            return view.View.pygame.Surface((self.width, self.height), view.View.pygame.SRCALPHA, 32)
        else:
            return view.View.pygame.Surface((self.width, self.height))

    def draw(self):
        surface = self.referance
        if self.convertalpha:
            surface.convert_alpha(self.referance)
        else:
            surface.fill(self.color)
            surface.set_alpha(self.alpha)

    def __del__(self):
        if self in Surface.surfaces:
            Surface.surfaces.remove(self)  # on l'enlève de nos tables de boutons avant de le détruire
            self.remove()

    def getSurfaces(cls):
        return Surface.surfaces

    getSurfaces = classmethod(getSurfaces)
