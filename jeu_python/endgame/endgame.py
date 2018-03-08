import constantes
import view as v
from uielements import surface as surface
import model
import functions as f
from coregame import coregame as coregame


class EndGame:
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

        # On supprime les elements graphiques - ATTENTION: Ils ne semblent pas tous se recree
        coregame.CoreGame.getCharacterSprites().clear()
        f.delete_menu_obj()

        # Retour au menu, après il devra etre sur un bouton
        model.Model.main_menu(False)
