import pygame
import uielement
import functions


class Image(uielement.UIelement):
    images = []

    """
    :param image_path - Le chemin vers l'image
    :param *UIargs - Tous les paramètres d'un élément graphique (voir classe "UIelement")
    """

    def __init__(self, image_path, *UIargs):
        uielement.UIelement.__init__(self, *UIargs, "Image")

        self.imagepath = functions.resource_path(image_path)
        self.originalimage = self.create(False)
        self.referance = self.create(True)  # on creer l'image pour avoir une référence vers celui-ci
        self.strip = None  # sous forme de liste uniquement si l'image est découpé en plusieurs
        self.currentimg = None  # n'existe que si strip existe, c'est le numéro de l'image à afficher, None s'il n'y a rien à afficher

        Image.images.append(self)

    def create(self, resize, xresize=None, yresize=None):
        image = pygame.image.load(self.imagepath).convert_alpha()
        if resize:
            image = pygame.transform.scale(image, (
                xresize or int(self.parentsurface.abswidth * self.scalew + self.width),
                yresize or int(self.parentsurface.absheight * self.scaleh + self.height)))
        return image

    def draw(self):
        originalimage = self.originalimage if self.strip is None else None if self.currentimg is None else self.strip[
            self.currentimg]
        if originalimage:
            self.referance = pygame.transform.scale(originalimage, (self.abswidth, self.absheight))
            self.referance = pygame.transform.rotate(self.referance, self.rotation)
            if self.alpha < 255:
                surf_real_size = (self.referance.get_width(), self.referance.get_height())
                temp = pygame.Surface(surf_real_size).convert()
                temp.blit(self.parentsurface.referance, (-self.absx, -self.absy))
                temp.blit(self.referance, (0, 0))
                temp.set_alpha(self.alpha)
                self.referance = temp
            self.visible = True
        else:
            self.visible = False

    def split(self, rects):
        self.strip = []
        self.currentimg = None
        for i in range(len(rects)):
            rec = pygame.Rect(rects[i])
            img = pygame.Surface(rec.size, pygame.SRCALPHA, 32).convert_alpha()
            img.blit(self.originalimage, (0, 0), rec)
            self.strip.append(img)

    def unreferance(self):
        Image.images.remove(self)
        self.remove()

    @classmethod
    def getImages(cls):
        return Image.images
