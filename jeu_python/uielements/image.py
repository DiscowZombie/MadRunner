import uielement
import view


class Image(uielement.UIelement):
    images = []

    """
    :param image_path - Le chemin vers l'image
    :param *UIargs - Tous les paramètres d'un élément graphique (voir classe "UIelement")
    """

    def __init__(self, image_path, *UIargs):
        uielement.UIelement.__init__(self, *UIargs, "Image")

        self.imagepath = image_path
        self.originalimage = self.create(False)
        self.referance = self.create(
            True)  # on creer l'image pour avoir une référence vers celui-ci, mais sans nécessairement l'afficher

        Image.images.append(self)

    def create(self, resize, xresize=None, yresize=None):
        image = view.View.pygame.image.load(self.imagepath)
        if resize:
            image = view.View.pygame.transform.scale(image, (
            xresize or int(self.parentsurface.abswidth * self.scalew + self.width),
            yresize or int(self.parentsurface.absheight * self.scaleh + self.height)))
        image.convert_alpha()
        return image

    def draw(self):
        self.referance = view.View.pygame.transform.scale(self.originalimage, (int(self.abswidth), int(self.absheight)))
        self.referance.convert_alpha()

    def unreferance(self):
        Image.images.remove(self)
        self.remove()

    def getImages(cls):
        return Image.images

    getImages = classmethod(getImages)
