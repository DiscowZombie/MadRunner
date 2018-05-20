import pygame

import uielement
import model
import constantes

from uielements import text as text


class Textbox(uielement.UIelement):
    textboxes = []

    def __init__(self, antialias, couleur_text, font, font_size, centeredx, centeredy,
                 offset, boxbordersize, boxbordercolor, maxchar, mdp, *UIargs):

        uielement.UIelement.__init__(self, *UIargs, "Textbox")

        self.text = ""
        self.antialias = antialias
        self.textcolor = couleur_text
        self.font = font
        self.fontsize = font_size
        self.textcenteredx = centeredx
        self.textcenteredy = centeredy
        self.textoffset = offset
        self.boxbordersize = boxbordersize
        self.boxbordercolor = boxbordercolor
        self.maxchar = maxchar
        self.mdp = mdp
        self.focused = False
        self.focustime = 0
        self.textobj = text.Text("", antialias, couleur_text, font, font_size, centeredx, centeredy,
                                 None, offset, False, *UIargs)
        self.referance = self.create()  # ATTENTION: La référence est la surface sur laquelle le rectangle du textbox est dessiné

        Textbox.textboxes.append(self)

    def focus(self):
        self.focused = True

    def unfocus(self):
        self.focused = False

    def addchar(self, char):
        new_text = self.text
        if char == "\r" or char == "\n" or char == "\r\n":  # touche entrée, dont le caractère varie selon la platforme.
            return
        elif char == "\b":
            new_text = new_text[:-1]
        else:
            if len(self.text) < self.maxchar:
                new_text += char
        self.text = new_text
        self.textobj.text = new_text

    def create(self):
        parentsurface = self.parentsurface
        if self.visible:
            rectangle = pygame.draw.rect(
                parentsurface.referance,
                self.color,
                [parentsurface.abswidth * self.scalex + self.x, parentsurface.absheight * self.scaley + self.y,
                 parentsurface.abswidth * self.scalew + self.width,
                 parentsurface.absheight * self.scaleh + self.height],
                self.bordersize
            )
            if self.boxbordersize > 0:
                pygame.draw.rect(
                    parentsurface.referance,
                    self.boxbordercolor,
                    [parentsurface.abswidth * self.scalex + self.x, parentsurface.absheight * self.scaley + self.y,
                     parentsurface.abswidth * self.scalew + self.width - 1,
                     parentsurface.absheight * self.scaleh + self.height - 1],
                    self.boxbordersize
                )
        else:
            rectangle = None
        if self.mdp:
            mdp = ""
            for i in range(len(self.text)):
                mdp += "*"
            self.textobj.text = mdp
        self.textobj.referance = self.textobj.create()
        return rectangle

    def draw(self):
        self.referance = self.create()
        if self.focused:
            draw_line = True
            self.focustime += model.Model.last_passed
            if self.focustime >= 1000:
                self.focustime = 0
            elif self.focustime >= 500:
                draw_line = False

            if draw_line:
                parentsurface = self.parentsurface
                text_size = self.textobj.textreferance.size(self.textobj.text)
                pygame.draw.line(
                    parentsurface.referance,
                    constantes.BLACK,
                    (parentsurface.abswidth * self.scalex + self.x + self.textoffset + text_size[0],
                     parentsurface.absheight * self.scaley + self.y + self.boxbordersize + 3),
                    (parentsurface.abswidth * self.scalex + self.x + self.textoffset + text_size[0],
                     parentsurface.absheight * self.scaley + self.y + self.absheight - self.boxbordersize - 3),
                    2
                )

    def unreferance(self):
        Textbox.textboxes.remove(self)
        self.remove()

    @classmethod
    def getTextboxes(cls):
        return Textbox.textboxes
