import uielement
import view


class Rect(uielement.UIelement):
    rects = []

    def __init__(self, *UIargs):
        uielement.UIelement.__init__(self, *UIargs, "Rect")

        self.referance = self.create()

        Rect.rects.append(self)

    def create(self):
        """referance = self.parentsurface.referance
        rectangle = referance.fill(self.color, [referance.get_width() * self.scalex + self.x, referance.get_height() * self.scaley + self.y,
             referance.get_width() * self.scalew + self.width, referance.get_height() * self.scaleh + self.height])"""
        parentsurface = self.parentsurface
        referance = parentsurface.referance
        rectangle = view.View.pygame.draw.rect(
            self.parentsurface.referance,
            self.color,
            [referance.get_width() * self.scalex + self.x, referance.get_height() * self.scaley + self.y,
             referance.get_width() * self.scalew + self.width, referance.get_height() * self.scaleh + self.height],
            self.bordersize
        )
        return rectangle

    def draw(self):
        self.referance = self.create()

    def unreferance(self):
        Rect.rects.remove(self)
        self.remove()
