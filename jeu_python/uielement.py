class UIelement:
    UIelements = {}

    """
    :param surface_bouton - La surface où sera l'élément graphique
    :param surface_position - La position de la surface où on va mettre l'élément graphique
    :param posx - La position x de l'élément graphique
    :param posy - La position y de l'élément graphique
    :param width - La largeur de l'élément graphique
    :param height - La hauteur de l'élément graphique
    :param color - La couleur d'arrière plan de l'élément graphique
    :param bordersize - Le taille de la bordure en pixel de l'élément graphique (s'il vaut 0, l'élément est repli)
    """

    def __init__(self, surface_bouton, surface_position, posx, posy, width, height, color, bordersize, classname,
                 alpha = None):
        self.x = posx
        self.y = posy
        self.absx = surface_position[
                        0] + posx  # position "absolue", càd, position par rapport à la fenêtre, et non la surface où on dessine l'élément
        self.absy = surface_position[1] + posy
        self.width = width
        self.height = height
        self.color = color
        self.bordersize = bordersize
        self.alpha = alpha
        self.classname = classname  # pas sûr que ce sera utile
        self.ismousein = False
        self.tweendata = None
        self.parentsurface = surface_bouton

        if not classname in UIelement.UIelements:
            UIelement.UIelements[classname] = []  # on l'ajoute aux éléments UI, en les triant par leur "classname"

        UIelement.UIelements[classname].append(self)

    def tween(self, posx, posy, width, height, duration,
              *otherattr):  # transition linéaire de la position et/ou de la taille, "duration" en secondes, on peut éventuellement fare une transition d'autres attributs
        self.tweendata = {
            "delta x": posx - self.x,
            "delta y": posy - self.y,
            "delta width": width - self.width,
            "delta height": height - self.height,
            "x start": self.x,
            "y start": self.y,
            "width start": self.width,
            "height start": self.height,
            "duration": duration,
            "passed": 0
        }

        if otherattr:  # pour ajouter des autres attributs à transitionner, mettre dans dans une liste un dictionnaire avec son nom ["name"] et sa valeur ["value"]
            if not "otherattr" in self.tweendata:
                self.tweendata["otherattr"] = []

            for attributdict in otherattr:
                attrname = attributdict["name"]
                attrvalue = attributdict["value"]
                currentattrvalue = self.__getattribute__(attrname)

                tweendict = {
                    "attrname": attrname,
                    "delta " + attrname: attrvalue - currentattrvalue,
                    attrname + " start": currentattrvalue
                }

                self.tweendata["otherattr"].append(tweendict)

    def remove(self):
        classlist = UIelement.UIelements[self.classname]
        if self in classlist:
            classlist.remove(self)
        del self

    def getUIelements(cls):
        return UIelement.UIelements

    getUIelements = classmethod(getUIelements)
