import pygame
import view as v
import constantes
import functions
from coregame import coregame as coregame
from uielements import image as image

haies = []

for i in range(10):
    haies.append(
        {
            "dist": 45 + 35*i,
            "touched": False,  # la haie est-elle renversée ?
            "obj": None
        }
    )

dimension_haie = None


def init():

    global dimension_haie

    for info_haie in haies:
        info_haie["touched"] = False  # reset la haie

    img_haie = pygame.image.load(functions.resource_path("assets/img/decors/" + coregame.CoreGame.carte + "/obstacle.png"))
    dimension_haie = (img_haie.get_width(), img_haie.get_height())
    coregame.CoreGame.dist_to_travel = 400
    coregame.CoreGame.disp_function = functions.computetime


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
                haie_obj = haieinfo["obj"]
                if not haieinfo["touched"]:
                    attrname = char.state + "sprite"
                    state_sprite = char.__getattribute__(attrname)
                    offset = (int(haie_obj.absx - (state_sprite.absx + state_sprite.offsetx)), int(haie_obj.absy - (state_sprite.absy + state_sprite.offsety)))
                    num_pix_col = state_sprite.masks[state_sprite.compteur].overlap_area(haie_obj.mask, offset)  # le nombre de pixels de collision entre la haie et le personnage
                    if num_pix_col and num_pix_col > 15:  # si le personnage touche la haie de plus de 15 pixels (car bon, toucher la haie de 1 pixel...)
                        haieinfo["touched"] = True
                        char.speed -= 0.35 * char.speed  # se prendre une haie réduit la vitesse de 35%
                        haie_obj.tween(  # transition de la rotation de la haie pour voir qu'elle tombe
                            0.2,
                            [
                                {
                                    "name": "y",
                                    "value": haie_obj.y + haie_obj.absheight//2
                                },
                                {
                                    "name": "rotation",
                                    "value": 90
                                }
                            ]
                        )
                delta_pix = (haieinfo["dist"] - distance) * 25  # nombre de pixel avant la haie par rapport au personnage
                pos_x_haie = char.absx - delta_pix
                haie_obj.x = pos_x_haie
        else:
            delta_pix = (haieinfo["dist"] - distance) * 25  # nombre de pixel avant la haie par rapport au personnage
            pos_x_haie = char.absx - delta_pix

            if pos_x_haie > - dimension_haie[0]:

                REPERTOIRE = "assets/img/decors/" + coregame.CoreGame.carte + "/obstacle.png"
                LARGEUR = dimension_haie[0]
                HAUTEUR = dimension_haie[1]
                POSITION_X = pos_x_haie
                POSITION_Y = char.y + 49 - dimension_haie[1]  # on va supposer que le personnage a toujours une hauteur de 98 pixels
                SCALE_X = 0
                SCALE_Y = 0.35
                SCALE_WIDTH = 0
                SCALE_HEIGHT = 0
                COULEUR = constantes.WHITE
                BORDURE = 0

                image_haie = image.Image(REPERTOIRE, v.View.screen, POSITION_X,
                                          POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                          BORDURE)
                image_haie.mask = pygame.mask.from_surface(image_haie.referance)

                haieinfo["obj"] = image_haie


def computescore():  # le score dépend du temps et du nombre de haies non renversées
    nb_passed = 0  # nombre de haies passé (càd sans le renverser)
    dist = coregame.CoreGame.distance
    for haieinfo in haies:
        if not haieinfo["touched"] and dist >= haieinfo["dist"]:
            nb_passed += 1
    return 100000000 / coregame.CoreGame.time + nb_passed*100
