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
        self.timeout = timeout  # le temps à partir duquel l'objet et détruit

        TAILLE_BOUTON = 30  # carré

        lettre = Key.availablekeys[random.randint(0,len(Key.availablekeys) - 1)]
        screenreferance = view.View.screen.referance
        screenwidth = screenreferance.get_width()
        surfaceheight = surface_boutons.referance.get_height()
        max_x_scale = (screenwidth - TAILLE_BOUTON)/screenwidth
        max_y_scale = (surfaceheight - TAILLE_BOUTON)/surfaceheight

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

        Key.availablekeys.remove(lettre)
        Key.keys.append(self)

    def canCreateKey(cls):  # peut-on créer un objet lettre ?
        return len(Key.availablekeys) > 0

    canCreateKey = classmethod(canCreateKey)
