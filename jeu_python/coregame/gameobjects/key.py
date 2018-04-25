import view
import constantes
import userstatistics

from uielements import text as text
from uielements import rect as rect
from coregame import coregame as coregame

import random


class Grid:

    def __init__(self):
        nb_key_x = view.View.screen.abswidth//(Key.keysize + 5) or 1  # espacemet de 5 pixels entre les boutons
        nb_key_y = coregame.CoreGame.current_core.surface_boutons.absheight//(Key.keysize + 5) or 1

        self.maxx = nb_key_x
        self.maxy = nb_key_y
        self.keys = []

    def removekey(self, key_obj):
        for keyinfo in self.keys:
            if keyinfo["key"] == key_obj:
                self.keys.remove(keyinfo)

    def updatecontent(self):
        if view.View.screen.updated:
            self.maxx = view.View.screen.abswidth//(Key.keysize + 5) or 1
            self.maxy = coregame.CoreGame.current_core.surface_boutons.absheight//(Key.keysize + 5) or 1
        for keyinfo in self.keys:
            num_x = keyinfo["position"] % self.maxx
            num_y = keyinfo["position"] // self.maxx
            if num_y > self.maxy:
                num_y = self.maxy  # bon, ça va faire bizarre ça quand même, mais bon... (les touches en dessous vont être "téléportées" plus haut
            pos_x = 5 + num_x*(Key.keysize + 5)
            pos_y = 5 + num_y*(Key.keysize + 5)
            rectref = keyinfo["key"].rectreferance
            textref = keyinfo["key"].textreferance
            rectref.x, textref.originalx = pos_x, pos_x
            rectref.y, textref.originaly = pos_y, pos_y


class EasyGrid(Grid):  # les touches apparaissent de gauche à droite, de haut en bas

    def __init__(self):
        Grid.__init__(self)

    def addkey(self, key_obj):
        pos_min = 0
        if len(self.keys) >= self.maxx * self.maxy:  # si la grille est rempli...
            pos_min = 0  # ... on se retrouve obligé de superposer 2 touches
        else:  # sinon, cela veut dire qu'il y a de la place pour la touche quelque part dans la grille !
            while True:
                valid = True
                for keyinfo in self.keys:
                    if keyinfo["position"] == pos_min:
                        pos_min += 1
                        valid = False
                if valid:
                    break

        self.keys.append(
            {
                "position": pos_min,
                "key": key_obj
            }
        )


class MediumGrid(Grid):  # les touches apparaissent n'importe où dans la grille

    def __init__(self):
        Grid.__init__(self)

    def addkey(self, key_obj):
        possible_pos = list(range(0, self.maxx * self.maxy - 1))  # les positions possibles pour la touche, sous forme de liste
        for keyinfo in self.keys:
            if keyinfo["position"] in possible_pos:  # il se peut que la position n'existe pas dans la liste des positions possibles (si 2 touches sur superposées)
                possible_pos.remove(keyinfo["position"])
        if len(possible_pos) == 0:  # si la grille est rempli...
            pos_grille = 0
        else:
            pos_grille = possible_pos[random.randint(0, len(possible_pos) - 1)]
        self.keys.append(
            {
                "position": pos_grille,
                "key": key_obj
            }
        )


class Key:

    keys = []  # les touches qui sont affiché à l'écran (et qu'il faut appuyer)
    grid = None  # la grille pour éviter le superposage de 2 touches (facile et moyen seulement)
    keysize = 30  # la taille d'une touche (carré)
    availablekeys = list(constantes.ALPHABET)  # les touches qui peuvent être affichées (pour éviter d'avoir 2 fois la même touches)
    avantages = ["energy", "speed"]  # les avantages possible (augmente la vitesse ou l'énergie)
    avantages_bonus = {  # l'intervalle d'augmentation possible de chaque avantage
        "energy": [5, 15],
        "speed": [0.05, 0.2]
    }

    def __init__(self, surface_boutons, timeout):

        self.time = 0  # temps depuis lequel l'objet a été créé
        self.timeout = timeout * 1000  # le temps à partir duquel l'objet et détruit (en ms)

        TAILLE_BOUTON = Key.keysize
        lettre = Key.availablekeys[random.randint(0, len(Key.availablekeys) - 1)]

        grille_obj = coregame.CoreGame.current_core.level_obj.grille
        if grille_obj:
            scalex = None
            scaley = None
        else:
            screenwidth = view.View.screen.abswidth
            surfaceheight = surface_boutons.absheight
            max_x_scale = (screenwidth - TAILLE_BOUTON) / screenwidth
            max_y_scale = (surfaceheight - TAILLE_BOUTON) / surfaceheight
            scalex = random.uniform(0, max_x_scale)
            scaley = random.uniform(0, max_y_scale)

        LARGEUR = TAILLE_BOUTON
        HAUTEUR = TAILLE_BOUTON
        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = scalex or 0
        SCALE_Y = scaley or 0
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.GRAY
        BORDURE = 0  # rempli

        rectreferance = rect.Rect(surface_boutons, POSITION_X, POSITION_Y, SCALE_X,
                                  SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                  BORDURE)

        TEXTE = lettre
        ANTIALIAS = True
        COULEUR = constantes.BLACK  # couleur du texte
        FONT = "Arial"
        TAILLE_FONT = 25
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = constantes.GRAY
        ECART = 0
        SEUL = True
        LARGEUR = TAILLE_BOUTON
        HAUTEUR = TAILLE_BOUTON
        POSITION_X = 0
        POSITION_Y = 0
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR_ARRIERE = constantes.GRAY
        BORDURE = 0

        textreferance = text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,
                                  SEUL,
                                  surface_boutons, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                  HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

        self.rectreferance = rectreferance
        self.textreferance = textreferance
        self.key = lettre

        grille_obj = coregame.CoreGame.current_core.level_obj.grille
        if grille_obj:
            grille_obj.addkey(self)
        Key.availablekeys.remove(lettre)
        Key.keys.append(self)

    def unreferance(self):
        grille_obj = coregame.CoreGame.current_core.level_obj.grille
        if grille_obj:
            grille_obj.removekey(self)
        self.rectreferance.unreferance()
        self.textreferance.unreferance()
        key_maj = self.key.capitalize()
        if not key_maj in Key.availablekeys:
            Key.availablekeys.append(key_maj)  # la lettre peut ainsi réapparaître
        Key.keys.remove(self)

    def getKeys(cls):
        return Key.keys

    def canCreateKey(cls):  # peut-on créer un objet lettre ?
        return len(Key.keys) < coregame.CoreGame.current_core.level_obj.maxkey

    def makegrid(cls, surface_boutons):
        print("make grid")

    def updatekeys(cls, passed):
        for key in Key.keys:
            key.time += passed
            if key.time >= key.timeout:
                key.unreferance()
                userstatistics.UserStatistics.stats.increment("missed_letters", 1)

    def keypressed(cls, pressed_key):
        exists = False
        prefix = "wrong"
        for key in Key.keys:
            if key.key == pressed_key:
                exists = True
                prefix = "correct"
                key.unreferance()
                break

        avantage = Key.avantages[random.randint(0, len(Key.avantages) - 1)]
        avantage_amount_table = Key.avantages_bonus[avantage]
        avantage_amount = random.uniform(avantage_amount_table[0], avantage_amount_table[1])
        if not exists:  # soustrait l'avantage (car la touche n'existe pas)
            avantage_amount = -avantage_amount

        coregame.Character.getCharacters()[0].boost(avantage, avantage_amount)  # ATENTION: NE MARCHE QU'EN MODE 1 JOUEUR !!!
        userstatistics.UserStatistics.stats.increment(prefix + "_letters", 1)

    getKeys = classmethod(getKeys)
    canCreateKey = classmethod(canCreateKey)
    makegrid = classmethod(makegrid)
    updatekeys = classmethod(updatekeys)
    keypressed = classmethod(keypressed)
