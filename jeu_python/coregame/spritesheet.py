# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

# TODO
#  http://www.pygame.org/wiki/Spritesheet


class spritesheet(object):
    sheet = None
    strip = []

    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def load(self, nombre_images):
        # Clear Strip
        self.strip = []

        lastmin = 3
        lastmax = 2 + 75
        for i in range(0, nombre_images + 1):
            self.strip.append(self.image_at((lastmin, 3, lastmax, 3 + 91)))
            lastmin += lastmax
            lastmax += (2 + 75 + 13)

        return self.strip

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image


class SpriteStripAnim(object):
    """sprite strip animator

    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """

    def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=1):
        """construct a SpriteStripAnim

        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.

        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.

        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        self.filename = filename
        ss = spritesheet(filename)
        self.images = ss.load_strip(rect, count, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames

    def iter(self):
        self.i = 0
        self.f = self.frames
        return self

    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image

    def __add__(self, ss):
        self.images.extend(ss.images)
        return self


import pygame
from pygame import *

pygame.init()

screen = pygame.display.set_mode((480, 320))

clock = pygame.time.Clock()

# http://www.pygame.org/wiki/Spritesheet
"""strips = [
    SpriteStripAnim("assets/img/personnages/gros/cour.png", (4, 4, 80, 89), 1, 1),
    SpriteStripAnim("assets/img/personnages/gros/cour.png", (80 * 7 + 4, 89 * 7 + 4, 80, 89), 1, 1)
]

n = 0
strips[n].iter()
image = strips[n].next()

while True:
    if n >= len(strips):
        n = 0
        strips[n].iter()

    screen.blit(image, (50, 50))
    pygame.display.flip()
    image = strips[n].next()

    clock.tick(1)"""

st = spritesheet("../assets/img/personnages/gros/cour.png").load(10)
n = 0

while True:
    screen.fill((0, 0, 0))

    screen.blit(st[n], (10, 10))
    if (n + 1 > (len(st) - 1)):
        n = 0
    else:
        n += 1

    pygame.display.flip()
    clock.tick(3) #1 fps
