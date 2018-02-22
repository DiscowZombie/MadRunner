# Source original (en tant que support)
#  http://www.pygame.org/wiki/Spritesheet

import pygame
import view


class SpriteSheet:

    def __init__(self, filename, posx, posy):
        self.sheet = view.View.pygame.image.load(filename).convert_alpha()
        self.x = posx
        self.y = posy

    def load(self, nombre_images, taille_frame):  # on va supposer pour l'instant que tous nos sprites défilent uniquement horizontalement
        # Clear Strip
        self.strip = []

        for i in range(0, nombre_images):
            self.strip.append(self.image_at((
                i * taille_frame[0],
                0,
                taille_frame[0],
                taille_frame[1]
            )))

        return self.strip

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        # Loads image from x,y,x+offset,y+offset
        rect = view.View.pygame.Rect(rectangle)
        image = view.View.pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, view.View.pygame.RLEACCEL)
        return image


class SpriteStripAnim(SpriteSheet):

    def __init__(self, spriteinfos, posx, posy):
        SpriteSheet.__init__(self, spriteinfos["image"], posx, posy)
        self.speedcounter = 0
        self.compteur = 0
        self.state = "run"
        self.speed = spriteinfos["initspeed"]
        self.numimage = spriteinfos["nbimage"]
        self.framesize = spriteinfos["framesize"]
        self.strip = self.load(self.numimage, self.framesize)

    def next(self, offsetx, offsety):
        # calcule et dessine la prochaine image (ou pas !)
        if self.speedcounter == 60//self.speed:
            self.speedcounter = 0
            self.compteur += 1
        else:
            self.speedcounter += 1

        if self.compteur == self.numimage:
            self.compteur = 0

        print(self.compteur)

        view.View.screen.referance.blit(self.strip[self.compteur], (self.x + offsetx, self.y + offsety))
