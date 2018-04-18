import pygame
import view as v
import constantes
import functions
from coregame import coregame as coregame
from uielements import image as image

haies_dist = []  # la distance à laquelle les haies sont

for i in range(10):
    haies_dist.append(45 + 35*i)


class Haie:

    haies = []

    def __init__(self, distance):
        self.distance = distance
        self.touched = False  # la haie est-elle renversée ?
        self.shown = False  # la haie est-elle dessinée ?
        self.image = None  # l'objet image de la haie (n'existe que lorque "shown" est sur True)
        Haie.haies.append(self)

    def show(self, posx, posy, width, height):
        self.shown = True

        REPERTOIRE = "assets/img/decors/" + coregame.CoreGame.current_core.carte + "/obstacle.png"
        LARGEUR = width
        HAUTEUR = height
        POSITION_X = posx
        POSITION_Y = posy
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
        self.image = image_haie

    def hide(self):
        self.shown = False
        self.image.unreferance()
        self.image = None

    def tombe(self):  # faire tomber la haie
        self.touched = True
        self.image.tween(  # transition de la rotation de la haie pour voir qu'elle tombe
            0.2,
            [
                {
                    "name": "y",
                    "value": self.image.y + self.image.absheight//2
                },
                {
                    "name": "rotation",
                    "value": 90
                }
            ]
        )

    def unreferance(self):
        if self.image:
            self.image.unreferance()
            self.image = None
        Haie.haies.remove(self)

    def getHaies(cls):
        return Haie.haies

    getHaies = classmethod(getHaies)


class _400mHaie:

    dist_to_travel = 400
    disp_function = None
    coursetype = "QH"

    def __init__(self):
        img_haie = pygame.image.load(functions.resource_path("assets/img/decors/" + coregame.CoreGame.current_core.carte + "/obstacle.png"))
        self.dimension_haie = (img_haie.get_width(), img_haie.get_height())
        _400mHaie.disp_function = functions.computetime

        for i in range(10):
            Haie(haies_dist[i])

    def refresh(self):
        distance = coregame.CoreGame.current_core.distance
        char = coregame.Character.getCharacters()[0]  # ATENTION: NE MARCHE QU'EN MODE 1 JOUEUR !!!

        """Déterminiation de s'il faut dessiner les haies ou pas"""
        for haie in Haie.getHaies():
            if haie.shown:
                if haie.image.absx > v.View.screen.abswidth or haie.image.absx + haie.image.abswidth < 0:  # efface les haie qui ne sont plus visibles
                    haie.hide()
                else:
                    if not haie.touched:
                        attrname = char.state + "sprite"
                        state_sprite = char.__getattribute__(attrname)
                        offset = (int(haie.image.absx - (state_sprite.absx + state_sprite.offsetx)), int(haie.image.absy - (state_sprite.absy + state_sprite.offsety)))
                        num_pix_col = state_sprite.masks[state_sprite.compteur].overlap_area(haie.image.mask, offset)  # le nombre de pixels de collision entre la haie et le personnage
                        if num_pix_col and num_pix_col > 15:  # si le personnage touche la haie de plus de 15 pixels (car bon, toucher la haie de 1 pixel...)
                            haie.tombe()
                            char.speed -= 0.35 * char.speed  # se prendre une haie réduit la vitesse de 35%
                    delta_pix = (haie.distance - distance) * 25  # nombre de pixel avant la haie par rapport au personnage
                    pos_x_haie = char.absx - delta_pix
                    haie.image.x = pos_x_haie
            else:
                delta_pix = (haie.distance - distance) * 25  # nombre de pixel avant la haie par rapport au personnage
                pos_x_haie = char.absx - delta_pix

                if pos_x_haie > - self.dimension_haie[0]:
                    haie.show(pos_x_haie, char.y + 49 - self.dimension_haie[1], self.dimension_haie[0], self.dimension_haie[1])  # on va supposer que le personnage a toujours une hauteur de 98 pixels)

    def computescore(self):  # le score dépend du temps et du nombre de haies non renversées
        nb_passed = 0  # nombre de haies passé (càd sans le renverser)
        dist = coregame.CoreGame.current_core.distance
        for haie in Haie.getHaies():
            if not haie.touched and dist >= haie.distance:
                nb_passed += 1
        return 100000000 / coregame.CoreGame.current_core.time + nb_passed*100

    def unreferance(self):
        for haie in list(Haie.getHaies()):
            haie.unreferance()
