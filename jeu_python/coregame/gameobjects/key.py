import view
import constantes
from uielements import text as text
from uielements import rect as rect
from coregame import coregame as coregame

import random


class Key:
    keys = []  # les touches qui sont affiché à l'écran (et qu'il faut appuyer)
    availablekeys = list(
        constantes.ALPHABET)  # les touches qui peuvent être affichées (pour éviter d'avoir 2 même touches)
    avantages = ["energy", "speed"]  # les avantages possible (augmente la vitesse ou l'énergie)
    avantages_bonus = {  # l'intervalle d'augmentation possible de chaque avantage
        "energy": [5, 15],
        "speed": [0.05, 0.2]
    }

    def __init__(self, surface_boutons, timeout):

        self.time = 0  # temps depuis lequel l'objet a été créé
        self.timeout = timeout * 1000  # le temps à partir duquel l'objet et détruit (en ms)

        TAILLE_BOUTON = 30  # carré

        lettre = Key.availablekeys[random.randint(0, len(Key.availablekeys) - 1)]
        screenwidth = view.View.screen.abswidth
        surfaceheight = surface_boutons.referance.get_height()
        max_x_scale = (screenwidth - TAILLE_BOUTON) / screenwidth
        max_y_scale = (surfaceheight - TAILLE_BOUTON) / surfaceheight

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

        textreferance = text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN, ECART,
                                  SEUL,
                                  surface_boutons, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                  HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

        self.rectreferance = rectreferance
        self.textreferance = textreferance
        self.absx = int(screenwidth * SCALE_X)
        self.absy = int(surfaceheight * SCALE_Y)
        self.key = lettre

        Key.availablekeys.remove(lettre)
        Key.keys.append(self)

    def unreferance(self):
        self.rectreferance.unreferance()
        self.textreferance.unreferance()
        key_maj = self.key.capitalize()
        if not key_maj in Key.availablekeys:
            Key.availablekeys.append(key_maj)  # la lettre peut ainsi réapparaître
        Key.keys.remove(self)

    def canCreateKey(cls):  # peut-on créer un objet lettre ?
        return len(Key.availablekeys) > 0

    def updatekeys(cls, passed):
        for key in Key.keys:
            key.time += passed
            if key.time >= key.timeout:
                key.unreferance()

    def keypressed(cls, pressed_key):
        keyobj = None
        for key in Key.keys:
            if key.key == pressed_key:
                keyobj = key
                key.unreferance()
                break

        avantage = Key.avantages[random.randint(0, len(Key.avantages) - 1)]
        avantage_amount_table = Key.avantages_bonus[avantage]
        avantage_amount = random.uniform(avantage_amount_table[0], avantage_amount_table[1])
        if not keyobj:  # soustrait l'avantage (car la touche n'existe pas)
            avantage_amount = -avantage_amount

        coregame.CoreGame.getCharacterSprites()[0].boost(avantage, avantage_amount)  # ATENTION: NE MARCHE QU'EN MODE 1 JOUEUR !!!

    canCreateKey = classmethod(canCreateKey)
    updatekeys = classmethod(updatekeys)
    keypressed = classmethod(keypressed)
