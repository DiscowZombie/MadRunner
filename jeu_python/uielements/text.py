import uielement
import view

class Text(uielement.UIelement):
    texts = []

    def __init__(self, text, antialias, couleur_text, font, font_size, centeredx, centeredy, backgroundcolor, offset,
                 *UIargs):

        uielement.UIelement.__init__(self, *UIargs, "Text")

        self.text = text
        self.antialias = antialias
        self.textcolor = couleur_text
        self.font = font
        self.fontsize = font_size
        self.textcenteredx = centeredx
        self.textcenteredy = centeredy
        self.backgroundcolor = backgroundcolor
        self.textoffset = offset
        self.create()

        Text.texts.append(self)

    def create(self):  # view
        texte = view.View.pygame.font.SysFont(self.font, self.fontsize)
        surfacetext = texte.render(self.text, self.antialias, self.textcolor,
                                   self.backgroundcolor)  # retourne la surface sur laquelle le texte est dessiné
        self.textreferance = texte
        self.referance = surfacetext

    def draw(self):
        self.create()

    def __del__(self):
        if self in Text.texts:
            Text.texts.remove(self)  # on l'enlève de nos tables de boutons avant de le détruire
            self.remove()

    def getTexts(cls):
        return Text.texts

    getTexts = classmethod(getTexts)
