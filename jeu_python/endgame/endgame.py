import constantes
import view as v
from uielements import surface as surface
from uielements import button as button


class EndGame:
    # Empêcher de mettre en pause SSI on est déjà arriver ici
    score = 0
    reason = None
    carte = None

    def __init__(self, modejeu, carte, distance, time, reason):
        if modejeu == "400m" or modejeu == "400 haie":
            """
            Exemples de score:
            
            Bon temps (0:50.000) -> 50000 => Score: 2k
            Mauvais temps (2:00:000) -> 200000 => Score: 500
            """
            self.score = (1 / time) * 100000000  # Prendre en compte la difficulité?
        else:
            self.score = distance * 100  # Prendre en compte la difficulité?
        self.carte = carte
        self.reason = reason

    def end(self):
        # Transition swag ?

        # Création de l'écran de fin

        # Surface
        LARGEUR = 500
        HAUTEUR = 420
        POSITION_X = 70
        POSITION_Y = 30
        SCALE_X = 0.05
        SCALE_Y = 0.03
        SCALE_WIDTH = 0.05  # TODO: A TRAVAILLER
        SCALE_HEIGHT = 0.03  # TODO: A TRAVAILLER
        COULEUR = constantes.WHITE
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = False

        surf = surface.Surface(ALPHA, CONVERT_ALPHA, v.View.screen, POSITION_X, POSITION_Y,
                               SCALE_X, SCALE_Y, LARGEUR,
                               HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                               BORDURE)

        # Créé une image propre et l'afficher - Image "End"
        # ...

        # Afficher des boutons
        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = 0
        HAUTEUR = 50
        SCALE_WIDTH = 1
        SCALE_HEIGHT = 0
        COULEUR = constantes.GRAY
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        ARRIERE_PLAN_TEXTE = COULEUR
        FONT = "Arial"
        TAILLE_FONT = 24
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = COULEUR
        ECART = 0
        BORDURE = 0  # rempli

        button.BRetourMenu("Retour", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                      ARRIERE_PLAN, ECART, surface, POSITION_X, POSITION_Y, SCALE_X,
                      SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
