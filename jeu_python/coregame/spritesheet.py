# Source original
#  http://www.pygame.org/wiki/Spritesheet

"""
3 pixels mort en haut
3 pixels mort en bas

80 pixels (aucun pixel mort), tout juste
"""
import view


class SpriteSheet(object):
    sheet = None
    strip = []

    def __init__(self, filename):
        self.sheet = view.View.pygame.image.load(filename).convert()

    def load(self, nombre_images):
        # Clear Strip
        self.strip = []

        x = 3
        for i in range(0, nombre_images):
            self.strip.append(self.image_at((
                i * 80,
                3,
                80,
                i * 80 + 76
            )))
            x += 88

        return self.strip

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        # Loads image from x,y,x+offset,y+offset
        rect = view.View.pygame.Rect(rectangle)
        image = view.View.pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, view.View.pygame.RLEACCEL)
        return image


class SpriteStripAnim(object):
    compteur = 0
    strip = []

    def __init__(self, strips):
        self.compteur = 0
        self.strip = strips

    def next(self, posx, posy):
        # Draw
        view.View.screen.blit(self.strip[self.compteur], (posx, posy))
        # Change compteur
        if self.compteur + 1 > (len(self.strip) - 1):
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
