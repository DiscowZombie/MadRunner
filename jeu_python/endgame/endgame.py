import constantes
import uielements.image as image
import view as v


class EndGame:
    score = 0
    reason = None
    carte = None

    def __init__(self, modejeu, carte, level, distance, time, reason):
        if modejeu == "400m" or modejeu == "400 haie":
            # Difficluté : 1 facile ; 2 moyen ; 3 difficile
            # Pour le moment, on a admet qu'elle vaut 2
            self.score = distance - (time * ((1 / 5) * 2))
        else:
            self.score = distance
        self.carte = carte
        self.reason = reason

    def end(self):
        # Création de l'écran de fin

        # TODO: Créé une image propre et l'afficher
        # Image "End"
        REPERTOIRE = "assets/img/end_screen.png"
        LARGEUR = 150
        HAUTEUR = 70
        POSITION_X = 90
        POSITION_Y = 200
        SCALE_X = 0
        SCALE_Y = 0
        SCALE_WIDTH = 1
        SCALE_HEIGHT = 1
        COULEUR = constantes.WHITE
        BORDURE = 0

        endimg = image.Image(REPERTOIRE, v.View.screen, POSITION_X,
                             POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                             BORDURE)

        # Affichage du son - Pour le moment dans la console, plus tard à l'écran
        print("Score: " + str(self.score))
