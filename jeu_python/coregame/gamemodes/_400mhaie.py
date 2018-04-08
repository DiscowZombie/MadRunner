import view as v
import constantes
from coregame import coregame as coregame
from uielements import image as image

haies = []

for i in range(10):
    haies.append(
        {
            "dist": 45 + 35*i,
            "obj": None
        }
    )


def refresh():
    distance = coregame.CoreGame.distance
    char = coregame.CoreGame.characters_sprite[0]  # ATENTION: NE MARCHE QU'EN MODE 1 JOUEUR !!!

    """Déterminiation de s'il faut dessiner les haies ou pas"""
    for haieinfo in haies:
        if haieinfo["obj"]:
            if haieinfo["obj"].absx > v.View.screen.abswidth or haieinfo["obj"].absx + haieinfo["obj"].abswidth < 0:  # efface les haie qui ne sont plus visibles
                haieinfo["obj"].unreferance()
                haieinfo["obj"] = None
            else:
                delta_pix = (haieinfo["dist"] - distance) * 10  # nombre de pixel avant la haie par rapport au personnage
                pos_x_haie = char.absx - delta_pix
                haieinfo["obj"].x = pos_x_haie
        else:
            delta_pix = (haieinfo["dist"] - distance) * 10  # nombre de pixel avant la haie par rapport au personnage
            pos_x_haie = char.absx - delta_pix

            if pos_x_haie > -20:
                REPERTOIRE = "assets/img/decors/Jeux Olympiques/obstacle.png"
                LARGEUR = 20
                HAUTEUR = 30
                POSITION_X = pos_x_haie
                POSITION_Y = char.y + LARGEUR//2
                SCALE_X = 0
                SCALE_Y = 0.35
                SCALE_WIDTH = 0
                SCALE_HEIGHT = 0
                COULEUR = constantes.WHITE
                BORDURE = 0

                haieinfo["obj"] = image.Image(REPERTOIRE, v.View.screen, POSITION_X,
                                          POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                          BORDURE)
