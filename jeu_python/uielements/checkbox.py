import uielement
import model
import view
import controller
import statemanager

from uielements import image
from uielements import surface
from uielements import text
import constantes


class Checkbox(uielement.UIelement):
    checkboxes = []

    """
    :param boxsize = la taille x du checkbox (carré)
    :param text - Le texte à côté du checkbox
    :param antialias - Y a-t-il l'anti-alias ou pas ?
    :param couleur_text - La couleur du texte
    :param font - Le font du texte
    :param font_size - La taille du font
    :param centeredx - Le texte est-il centré sur l'axe x ?
    :param centeredy - Le texte est-il centré sur l'axe y ?
    :param backgroundcolor - La couleur d'arrière plan de la surface sur laquelle le texte va être mis
    :param offset - Le nombre de pixel de décalage du texte sur l'axe x
    :param *UIargs - Tous les paramètres d'un élément graphique (voir classe "UIelement")
    """

    def __init__(self, boxsize, text, antialias, couleur_text, font, font_size, centeredx, centeredy, backgroundcolor, offset,
                 *UIargs):

        uielement.UIelement.__init__(self, *UIargs, "Checkbox")

        self.boxsize = boxsize
        self.text = text
        self.antialias = antialias
        self.textcolor = couleur_text
        self.font = font
        self.fontsize = font_size
        self.textcenteredx = centeredx
        self.textcenteredy = centeredy
        self.backgroundcolor = backgroundcolor
        self.textoffset = boxsize + offset
        self.checked = False
        self.clicking = False
        self.create()  # la référence est crée en appelant cela. ATTENTION: La référence est la surface sur laquelle le texte est dessinée

        Checkbox.checkboxes.append(self)

    def create(self):
        posy = self.y + int(self.height/2 - self.boxsize/2)
        view.View.pygame.draw.rect(self.parentsurface, constantes.WHITE, [self.x, posy, self.boxsize, self.boxsize],
                             0)
        view.View.pygame.draw.rect(self.parentsurface, self.color, [self.x, posy, self.boxsize, self.boxsize],
                             self.bordersize)
        text.Text.create(self)
        if self.checked:
            self.checkreferance = image.Image.create(self, True, self.boxsize, self.boxsize)
