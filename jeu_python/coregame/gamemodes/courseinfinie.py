import pygame
import view as v
import functions
import constantes
import userstatistics

import random

from coregame import coregame as coregame
from uielements import image as image


class Obstacle:

    obstacles = []

    def __init__(self, distance):
        self.distance = distance
        self.touched = False  # l'obstacle est-il renversé ?
        self.shown = False  # l'obstacle est-il dessiné ?
        self.passed = False  # l'obstacle a-t-il été passé ?
        self.image = None  # l'objet image de l'obstacle (n'existe que lorque "shown" est sur True)
        Obstacle.obstacles.append(self)

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

        image_obstacle = image.Image(REPERTOIRE, v.View.screen, POSITION_X,
                                  POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                  BORDURE)
        image_obstacle.mask = pygame.mask.from_surface(image_obstacle.referance)
        self.image = image_obstacle

    def tombe(self):  # faire tomber l'obstacle
        self.touched = True
        self.image.tween(  # transition de la rotation de l'obstacle pour voir qu'il tombe
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
        Obstacle.obstacles.remove(self)

    def getObstacles(cls):
        return Obstacle.obstacles

    getObstacles = classmethod(getObstacles)


class CourseInfinie:

    dist_to_travel = None
    disp_function = None
    score_text = "Distance"
    coursetype = "I"

    def __init__(self):
        img_obstacle = pygame.image.load(functions.resource_path("assets/img/decors/" + coregame.CoreGame.current_core.carte + "/obstacle.png"))
        self.dimension_obstacle = (img_obstacle.get_width(), img_obstacle.get_height())
        self.farthest = 20  # la distace de l'obstacle le plus éloigné de la ligne de départ
        self.nb_passed = 0  # nombre d'obstacles passés (càd sans le renverser)
        CourseInfinie.disp_function = functions.computedistance
        Obstacle(self.farthest)  # premier obstacle à 20 mètres de la ligne de départ
        self.next_obstacle = self.farthest + 35*random.randint(5, 10)/10
        self.caught = False

        POSITION_X = 0
        POSITION_Y = 65
        SCALE_X = 0.85
        SCALE_Y = 0.35
        INITDIST = - 2

        self.courseur = coregame.Character(constantes.CharactersFeatures["normal"], constantes.Animations["poursuiveur"], POSITION_X, POSITION_Y,
                  SCALE_X, SCALE_Y, INITDIST)

    def refresh(self):

        distance = coregame.CoreGame.current_core.distance
        char = coregame.Character.getCharacters()[0]  # ATENTION: NE MARCHE QU'EN MODE 1 JOUEUR !!!

        if not self.caught and distance - self.courseur.distance <= 1.75:
            self.caught = True
            coregame.CoreGame.current_core.end(True)
            return

        for obstacle in Obstacle.getObstacles():
            if obstacle.shown:
                if obstacle.image.absx > v.View.screen.abswidth and obstacle.distance < distance:  # efface les obstacles qui ne sont plus visibles
                    obstacle.unreferance()
                else:
                    if not obstacle.touched:
                        attrname = char.state + "sprite"
                        state_sprite = char.__getattribute__(attrname)
                        offset = (int(obstacle.image.absx - (char.absx + state_sprite.x)), int(obstacle.image.absy - (char.absy + state_sprite.y)))
                        num_pix_col = state_sprite.masks[state_sprite.compteur].overlap_area(obstacle.image.mask, offset)  # le nombre de pixels de collision entre l'obstacle et le personnage
                        if num_pix_col and num_pix_col > 15:  # si le personnage touche l'obstacle de plus de 15 pixels (car bon, toucher l'obstacle de 1 pixel...)
                            obstacle.tombe()
                            char.speed -= 0.35 * char.speed  # se prendre un obstacle réduit la vitesse de 35%
                    delta_pix = (obstacle.distance - distance) * 25  # nombre de pixel avant l'obstacle par rapport au personnage
                    pos_x_haie = char.absx - delta_pix
                    obstacle.image.x = pos_x_haie
                    if not obstacle.passed and obstacle.image.absx >= char.absx + 40:  # on va supposer que le personnage a toujours une largeur de 80 pixels
                        obstacle.passed = True
                        if not obstacle.touched:
                            self.nb_passed += 1
            else:
                delta_pix = (obstacle.distance - distance) * 25  # nombre de pixel avant l'obstacle par rapport au personnage
                pos_x_obstacle = char.absx - delta_pix

                if pos_x_obstacle > - self.dimension_obstacle[0]:
                    obstacle.show(pos_x_obstacle, char.y + 49 - self.dimension_obstacle[1], self.dimension_obstacle[0], self.dimension_obstacle[1])  # on va supposer que le personnage a toujours une hauteur de 98 pixels

        distleft = distance + (char.absx / 25)  # distance à gauche de l'écran de la ligne de départ
        if distleft >= self.next_obstacle:
            Obstacle(self.next_obstacle)
            self.farthest = self.next_obstacle
            self.next_obstacle = self.farthest + 35*random.randint(5, 15)/10

        self.courseur.speed = distance/distance**0.73

    def computescore(self):  # le score dépend de la distance parcourue et du nombre d'obstacles non renversées
        dist = coregame.CoreGame.current_core.distance
        return dist + 100 * self.nb_passed

    def isrecord(self, gm_score):
        return gm_score > userstatistics.UserStatistics.stats.best_gm_score["Course infinie"]

    def unreferance(self):
        for obstacle in list(Obstacle.getObstacles()):
            obstacle.unreferance()

    def computekeychance(cls):
        distance = coregame.CoreGame.current_core.distance
        return 1 + int(distance ** 0.25 / distance * 500)

    computekeychance = classmethod(computekeychance)
