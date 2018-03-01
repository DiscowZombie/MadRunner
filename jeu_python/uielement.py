class UIelement:
    UIelements = {}

    """
    :param surface_bouton - L'objet de la surface où sera placé l'élément graphique
    :param surface_position - La position de la surface où on va mettre l'élément graphique
    :param posx - La position x de l'élément graphique
    :param posy - La position y de l'élément graphique
    :param scalex - La position x de l'élément graphique (proportionnelle à la taille de l'écran, entre 0 et 1)
    :param scaley - La position y de l'élément graphique (proportionnelle à la taille de l'écran, entre 0 et 1)
    :param width - La largeur de l'élément graphique
    :param height - La hauteur de l'élément graphique
    :param scalew - La largeur de l'élément graphique (proportionnelle à la taille de l'écran, entre 0 et 1)
    :param scaleh - La hauteur de l'élément graphique (proportionnelle à la taille de l'écran, entre 0 et 1)
    :param color - La couleur d'arrière plan de l'élément graphique
    :param bordersize - Le taille de la bordure en pixel de l'élément graphique (s'il vaut 0, l'élément est repli)
    """

    def __init__(self, surface_obj, posx, posy, scalex, scaley, width, height, scalew, scaleh, color, bordersize, classname,
                 alpha = None, isscreen = False):
        self.x = posx
        self.y = posy
        if isscreen:  # petite exception pour l'objet écran, car celui-ci n'a pas de descendant, donc ça pose problème pour les positions et tailles absolues (qui dépendent des valeurs des parents)
            self.absx = 0
            self.absy = 0
            self.abswidth = width
            self.absheight = height
        else:
            self.absx = int(surface_obj.absx + surface_obj.abswidth*scalex + posx)  # position "absolue", càd, position par rapport à la fenêtre, et non la surface où on dessine l'élément
            self.absy = int(surface_obj.absy + surface_obj.absheight*scaley + posy)
            self.abswidth = int(surface_obj.abswidth*scalew + width)
            self.absheight = int(surface_obj.absheight*scaleh + height)

        self.scalex = scalex
        self.scaley = scaley
        self.width = width
        self.height = height
        self.scalew = scalew
        self.scaleh = scaleh
        self.color = color
        self.bordersize = bordersize
        self.alpha = alpha
        self.classname = classname  # pas sûr que ce sera utile
        self.ismousein = False
        self.tweendata = None
        self.children = []  # pour ajouter des éléments graphiques dans d'autres

        if not isscreen:
            surface_obj.addchild(self)  # appeler cette méthode va ajouter un attribut appelé "parentsurface" qui permet d'avoir une référence vers l'objet parent
            if not classname in UIelement.UIelements:
                UIelement.UIelements[classname] = []
            UIelement.UIelements[classname].append(self)  # on l'ajoute aux éléments UI, en les triant par leur "classname"

    def addchild(self, child):  # pour ajouter un élément graphique dans un autre (ex: un bouton dans une surface)
        self.children.append(child)
        child.parentsurface = self

    def tween(self, posx, posy, scalex, scaley, width, height, scalew, scaleh, duration,
              *otherattr):  # transition linéaire de la position et/ou de la taille, "duration" en secondes, on peut éventuellement fare une transition d'autres attributs
        self.tweendata = {
            "delta x": posx - self.x,
            "delta y": posy - self.y,
            "delta x scale": scalex - self.scalex,
            "delta y scale": scaley - self.scaley,
            "delta width": width - self.width,
            "delta height": height - self.height,
            "delta width scale": scalew - self.scalew,
            "delta height scale": scaleh - self.scaleh,
            "x start": self.x,
            "y start": self.y,
            "scale x start": self.scalex,
            "scale y start": self.scaley,
            "width start": self.width,
            "height start": self.height,
            "scale width start": self.scalew,
            "scale height start": self.scaleh,
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
        for child in self.children:  # ne pas oublier d'effacer également les objets descendants de celui-ci
            child.remove()
        if self in self.parentsurface.children:
            self.parentsurface.children.remove(self)  # on l'enlève également de la table des descendants de son parent
        if self in classlist:
            classlist.remove(self)
        del self

    def getUIelements(cls):
        return UIelement.UIelements

    getUIelements = classmethod(getUIelements)
