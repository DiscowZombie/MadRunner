import view
import constantes
from uielements import text as text
from uielements import rect as rect

import random


class Key():

    keys = []  # les touches qui sont affiché à l'écran (et qu'il faut appuyer)
    availablekeys = list(constantes.ALPHABET)  # les touches qui peuvent être affichées (pour éviter d'avoir 2 même touches)

    def __init__(self, surface_boutons, timeout):

        self.time = 0  # temps depuis lequel l'objet a été créé
        self.timeout = timeout*1000  # le temps à partir duquel l'objet et détruit (en ms)

        TAILLE_BOUTON = 30  # carré

        lettre = Key.availablekeys[random.randint(0,len(Key.availablekeys) - 1)]
        screenreferance = view.View.screen.referance
        screenwidth = screenreferance.get_width()
        surfaceheight = surface_boutons.referance.get_height()
        max_x_scale = (screenwidth - TAILLE_BOUTON)/screenwidth
        max_y_scale = (surfaceheight - TAILLE_BOUTON)/surfaceheight

        """DEMANDER A MR LANGER POUR CA ! COMMENT FAIRE POUR VERIFIER LES POSITIONS POSSIBLES AFIN DE NE PAS SUPERPOSER 2 SURFACES !"""

        """impossible_position_ranges = []

        for keyobj in Key.keys:
            x = keyobj.absx
            y = keyobj.absy

            impossible_position_ranges.append(((x - TAILLE_BOUTON, x + TAILLE_BOUTON), (y - TAILLE_BOUTON, y + TAILLE_BOUTON)))

        possible_position_ranges = []

        for impossible_range in impossible_position_ranges:
            for impossible_range2 in impossible_position_ranges:
                if impossible_range != impossible_range2:"""


        LARGEUR = TAILLE_BOUTON
        HAUTEUR = TAILLE_BOUTON
        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = random.uniform(0, max_x_scale)
        SCALE_Y = random.uniform(0, max_y_scale)
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

        textreferance = text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART, SEUL,
                           surface_boutons, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                           HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

        self.rectreferance = rectreferance
        self.textreferance = textreferance
        self.absx = int(screenwidth * SCALE_X)
        self.absy = int(surfaceheight * SCALE_Y)
        self.key = lettre

        Key.availablekeys.remove(lettre)
        Key.keys.append(self)

    def __del__(self):
        self.rectreferance.__del__()
        self.textreferance.__del__()
        if self in Key.keys:
            Key.keys.remove(self)
        del self

    def canCreateKey(cls):  # peut-on créer un objet lettre ?
        return len(Key.availablekeys) > 0

    def updatekeys(cls, passed):
        for key in Key.keys:
            key.time += passed
            if key.time >= key.timeout:
                key.__del__()

    def keypressed(cls, pressed_key):
        exists = False
        for key in Key.keys:
            if key.key == pressed_key:
                exists = True
                key.__del__()
                break

        if exists:
            """Donne l'avantage"""
        else:
            """fait le contraire de l'avantage"""

    canCreateKey = classmethod(canCreateKey)
    updatekeys = classmethod(updatekeys)
    keypressed = classmethod(keypressed)
