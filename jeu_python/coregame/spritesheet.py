# Source original (en tant que support)
#  http://www.pygame.org/wiki/Spritesheet

import view


class SpriteSheet:
    sheet = None
    strip = []

    def __init__(self, filename):
        self.sheet = view.View.pygame.image.load(filename).convert_alpha()

    def load(self, nombre_images):
        # Clear Strip
        self.strip = []

        for i in range(0, nombre_images):
            self.strip.append(self.image_at((
                i * 80,
                0,
                80,
                98
            )))

        return self.strip

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        # Loads image from x,y,x+offset,y+offset
        rect = view.View.pygame.Rect(rectangle)
        image = view.View.pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, view.View.pygame.RLEACCEL)
        return image


class SpriteStripAnim(SpriteSheet):

    def __init__(self, spriteinfos):
        SpriteSheet.__init__(self, spriteinfos["image"])
        self.compteur = 0
        self.speed = spriteinfos["initspeed"]
        self.numimage = spriteinfos["nbimage"]
        self.strip = self.load(self.numimage)

    def next(self, posx, posy):
        # Draw
        # ne pas oublier de passer à l'image suivante uniquement si la vitesse le permet, ne pas oublier d'ajuter ca !
        view.View.screen.referance.blit(self.strip[self.compteur], (posx, posy))
        # Change compteur
        if self.compteur + 1 == self.numimage:
            self.compteur = 0
        else:
            self.compteur += 1


"""
Version indé
import pygame
from pygame import *

pygame.init()

screen = pygame.display.set_mode((480, 320))
clock = pygame.time.Clock()

st = SpriteSheet("../assets/img/personnages/gros/cour.png").load(10)
ssa = SpriteStripAnim(st)

while True:
    screen.fill((0, 0, 0))

    # Le perso doit bouger à 15 fps
    for i in range(0, 60//4):
        ssa.next(100, 100)
        pygame.time.wait(33)

    pygame.display.flip()
    clock.tick(60)
"""
