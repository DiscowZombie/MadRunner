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
        self.referance = self.create(True)  # on creer l'image pour avoir une référence vers celui-ci, mais sans nécessairement l'afficher

        Image.images.append(self)

    def create(self, resize):
        image = view.View.pygame.image.load(self.imagepath).convert_alpha()
        if resize:
            image = view.View.pygame.transform.scale(image, (self.width, self.height))
        return image

    def draw(self):
        self.referance = view.View.pygame.transform.scale(self.originalimage, (self.width, self.height))

    def __del__(self):
        if self in Image.images:
            Image.images.remove(self)  # on l'enlève de nos tables de boutons avant de le détruire
            self.remove()

    def getImages(cls):
        return Image.images

    getImages = classmethod(getImages)
