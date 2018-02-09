# Source original
#  http://www.pygame.org/wiki/Spritesheet

"""
3 pixels mort en haut
3 pixels mort en bas

80 pixels (aucun pixel mort), tout juste
"""


class SpriteSheet(object):
    sheet = None
    strip = []

    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def load(self, nombre_images):
        # Clear Strip
        self.strip = []

        x = 3
        for i in range(0, nombre_images):
            self.strip.append(self.image_at((x, 3, x + 80, 76)))
            x += 88

        return self.strip

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        # Loads image from x,y,x+offset,y+offset
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image


class SpriteStripAnim(object):
    compteur = 0
    strip = []

    def __init__(self, strips):
        self.compteur = 0
        self.strip = strips

    def next(self, posx, posy):
        screen.blit(self.strip[self.compteur], (posx, posy))
        if self.compteur + 1 > (len(self.strip) - 1):
            self.compteur = 0
        else:
            self.compteur += 1


import pygame
from pygame import *

pygame.init()

screen = pygame.display.set_mode((480, 320))
clock = pygame.time.Clock()

st = SpriteSheet("../assets/img/personnages/gros/cour.png").load(10)
ssa = SpriteStripAnim(st)
n = 0

while True:
    screen.fill((0, 0, 0))

    ssa.next(100, 100)

    pygame.display.flip()
    clock.tick(3)  # 3 fps
