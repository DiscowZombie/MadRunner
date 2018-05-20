import pygame
import uielement
import functions as f


class Text(uielement.UIelement):
    texts = []

    def __init__(self, text, antialias, couleur_text, font, font_size, centeredx, centeredy, backgroundcolor, offset,
                 alone, *UIargs):

        uielement.UIelement.__init__(self, *UIargs, "Text")

        if alone:
            self.originalx = self.x
            self.originaly = self.y

        self.text = text
        self.antialias = antialias
        self.textcolor = couleur_text
        self.font = font
        self.fontsize = font_size
        self.textcenteredx = centeredx
        self.textcenteredy = centeredy
        self.backgroundcolor = backgroundcolor
        self.textoffset = offset
        self.alone = alone
        self.recreate = False  # permet de savoir s'il faut recréer le texte
        self.textreferance = pygame.font.Font(open(f.resource_path("assets/fonts/" + font + ".ttf"), "rb"), font_size)
        self.referance = self.create()

        Text.texts.append(self)

    def __setattr__(self, key,
                    value):  # pour des raisons de performances, on va vérifier certaines choses lorqu'on affecte une valeur à un attribut
        if hasattr(self, key):
            if (key == "font" or key == "fontsize") and getattr(self,
                                                                key) != value:  # si l'un de ces attributs est changé et que la nouvelle valeur est différente
                self.recreate = True
        self.__dict__[key] = value

    def create(self):  # view
        texte = self.textreferance
        surfacetext = texte.render(self.text, self.antialias, self.textcolor,
                                   self.backgroundcolor)  # retourne la surface sur laquelle le texte est dessiné
        if self.textcenteredx or self.textcenteredy:
            positionx, positiony = f.centretexte(texte.size(self.text), (self.abswidth, self.absheight))
            if not self.textcenteredx:
                positionx = 0
            if not self.textcenteredy:
                positiony = 0
        else:
            positionx, positiony = 0, 0

        if self.alone:
            self.x = self.originalx + positionx + self.textoffset
            self.y = self.originaly + positiony
        else:
            self.x = positionx + self.textoffset
            self.y = positiony

        return surfacetext.convert_alpha()

    def draw(self):
        if self.recreate:
            self.recreate = False
            self.textreferance = pygame.font.Font(open(f.resource_path("assets/fonts/" + self.font + ".ttf"), "rb"),
                                                  int(self.fontsize))
        if self.alone:  # si l'objet texte fait partie d'un autre objet (ex: bouton), on laisse l'autre objet se charger de l'apparition du texte
            self.referance = self.create()

    def unreferance(self):
        Text.texts.remove(self)
        self.remove()

    @classmethod
    def getTexts(cls):
        return Text.texts
