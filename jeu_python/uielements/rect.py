import uielement
import view


class Rect(uielement.UIelement):
    rects = []

    def __init__(self, *UIargs):
        uielement.UIelement.__init__(self, *UIargs, "Rect")

        self.referance = self.create()

        Rect.rects.append(self)

    def create(self):
        """parentsurface = self.parentsurface
        rectangle = parentsurface.referance.fill(self.color, [parentsurface.abswidth * self.scalex + self.x, parentsurface.absheight * self.scaley + self.y,
             parentsurface.abswidth * self.scalew + self.width, parentsurface.absheight * self.scaleh + self.height])"""
        parentsurface = self.parentsurface
        rectangle = view.View.pygame.draw.rect(
            parentsurface.referance,
            self.color,
            [parentsurface.abswidth * self.scalex + self.x, parentsurface.absheight * self.scaley + self.y,
             parentsurface.abswidth * self.scalew + self.width, parentsurface.absheight * self.scaleh + self.height],
            self.bordersize
        )
        return rectangle

    def draw(self):
        self.referance = self.create()

    def unreferance(self):
        Rect.rects.remove(self)
        self.remove()
