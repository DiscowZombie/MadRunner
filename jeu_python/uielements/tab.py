import pygame

import uielement
import functions
import constantes

from uielements import text as text
from uielements import image as image


class Tab(uielement.UIelement):
    tabs = []

    def __init__(self, name, textb, antialias, couleur_text, backgroundtextcolor, font, font_size, centeredx, centeredy,
                 backgroundselectcolor, backgroundunselectcolor, offset, imagepath, *UIargs):

        uielement.UIelement.__init__(self, *UIargs, "Tab")

        self.name = name
        self.text = textb
        self.antialias = antialias
        self.textcolor = couleur_text
        self.backgroundtextcolor = backgroundtextcolor
        self.font = font
        self.fontsize = font_size
        self.textcenteredx = centeredx
        self.textcenteredy = centeredy
        self.backgroundselectcolor = backgroundselectcolor
        self.backgroundunselectcolor = backgroundunselectcolor
        self.textoffset = offset
        self.image = image
        self.selected = False
        self.linkedtabs = []  # ceci est une liste des tabs qui sont "liés" à celui-ci, c'est à dire, si ce tab est sélectionné mais qu'un des tab lié est sélectionné, l'autre ce tab va être désélectionné.
        self.textobj = text.Text(textb, antialias, couleur_text, font, font_size, centeredx, centeredy,
                                 backgroundtextcolor, offset, False, *UIargs)
        if imagepath:
            self.imagepath = functions.resource_path(imagepath)
            self.imagereferance = image.Image.create(self, True, self.height - 10, self.height - 10)
        else:
            self.imagereferance = None
        self.referance = self.create()  # ATTENTION: La référence est la surface sur laquelle le rectangle du tab est dessiné

        Tab.tabs.append(self)

    def select(self, default=None):
        self.selected = True
        if not default:
            for tab in self.linkedtabs:
                tab.selected = False
            self.button1down()

    def getOtherSelectedTabs(self):
        othertabs = []
        for tab in Tab.getTabs():
            if tab.selected and tab.name != self.name:
                othertabs.append(tab)
        return othertabs

    def create(self):
        parentsurface = self.parentsurface
        if self.visible:
            yoffset = 0
            if self.selected:
                color = self.backgroundselectcolor
                yoffset = -5  # 5 pixels plus haut
            else:
                color = self.backgroundunselectcolor
            rectangle = pygame.draw.rect(
                self.parentsurface.referance,
                color,
                [parentsurface.abswidth * self.scalex + self.x,
                 parentsurface.absheight * self.scaley + self.y + yoffset,
                 parentsurface.abswidth * self.scalew + self.width,
                 parentsurface.absheight * self.scaleh + self.height - yoffset],
                self.bordersize
            )

            # Contours du tab
            pygame.draw.line(  # haut
                self.parentsurface.referance,
                constantes.BLACK,
                (self.x, self.y + yoffset),
                (self.x + self.width - 1, self.y + yoffset)
            )
            pygame.draw.line(  # gauche
                self.parentsurface.referance,
                constantes.BLACK,
                (self.x, self.y + yoffset),
                (self.x, self.y + self.height)
            )
            pygame.draw.line(  # droite
                self.parentsurface.referance,
                constantes.BLACK,
                (self.x + self.width - 1, self.y + yoffset),
                (self.x + self.width - 1, self.y + self.height),
            )
        else:
            rectangle = None
        self.textobj.create()
        return rectangle

    def draw(self):
        self.referance = self.create()

    def unreferance(self):
        self.linkedtabs.clear()
        Tab.tabs.remove(self)
        self.remove()

    def getTabs(cls):
        return Tab.tabs

    def linktabs(cls, *tabs):
        for tab in tabs:
            for othertab in tabs:
                if tab.name != othertab.name:
                    tab.linkedtabs.append(othertab)

    getTabs = classmethod(getTabs)
    linktabs = classmethod(linktabs)


class TMeilleurScoreLocal(Tab):
    def __init__(*arguments):
        Tab.__init__(*arguments)

    def button1down(self):
        level = self.getOtherSelectedTabs()[0].name
        functions.displaybestscore("Personnel", level)


class TMeilleurScoreEnLigne(Tab):
    def __init__(*arguments):
        Tab.__init__(*arguments)

    def button1down(self):
        level = self.getOtherSelectedTabs()[0].name
        functions.displaybestscore("Global", level)


class TFacile(Tab):
    def __init__(*arguments):
        Tab.__init__(*arguments)

    def button1down(self):
        stype = self.getOtherSelectedTabs()[0].name
        functions.displaybestscore(stype, "Facile")


class TMoyen(Tab):
    def __init__(*arguments):
        Tab.__init__(*arguments)

    def button1down(self):
        stype = self.getOtherSelectedTabs()[0].name
        functions.displaybestscore(stype, "Moyen")


class TDifficile(Tab):
    def __init__(*arguments):
        Tab.__init__(*arguments)

    def button1down(self):
        stype = self.getOtherSelectedTabs()[0].name
        functions.displaybestscore(stype, "Difficile")
