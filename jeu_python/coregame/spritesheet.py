# Source original (en tant que support)
#  http://www.pygame.org/wiki/Spritesheet
import functions as f
import pygame
import view


class SpriteSheet:

    def __init__(self, filename):
        self.sheet = view.View.pygame.image.load(filename).convert_alpha()

    def load(self, nombre_images, taille_frame):  # on va supposer pour l'instant que tous nos sprites défilent uniquement horizontalement
        # Clear Strip
        strip = []
        masks = []

        for i in range(0, nombre_images):
            image = self.image_at((
                i * taille_frame[0],
                0,
                taille_frame[0],
                taille_frame[1]
            ))
            strip.append(image)
            masks.append(pygame.mask.from_surface(image))

        return strip, masks

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

    sprite_anims = []

    def __init__(self, spriteinfos):
        SpriteSheet.__init__(self, spriteinfos["image"])
        self.x = spriteinfos["framesize"][0]//2
        self.y = spriteinfos["framesize"][1]//2
        self.speedcounter = 0
        self.compteur = 0
        self.totalcompteur = 0
        self.time = 0
        self.state = "run"
        self.speed = spriteinfos["initspeed"]
        self.numimage = spriteinfos["nbimage"]
        self.framesize = spriteinfos["framesize"]
        self.repeatimage = spriteinfos["repeatimage"]
        self.strip, self.masks = self.load(self.numimage, self.framesize)

        SpriteStripAnim.sprite_anims.append(self)

    def next(self, passed):  # calcule et dessine la prochaine image (ou pas !)
        if self.speedcounter >= 60//self.speed:
            self.speedcounter = 0
            self.compteur += 1
        else:
            self.speedcounter += 1

        if self.compteur == self.numimage:
            self.compteur = self.repeatimage - 1

        self.totalcompteur += 1
        self.time += passed

    def updatepos(self, x, y):  # mis à jour de la position du sprite (par rapport à la position du personnage)
        self.x = -int(self.framesize[0]/2) + x
        self.y = -int(self.framesize[1]/2) + y

    def reset(self):
        self.totalcompteur = 0
        self.compteur = 0
        self.speedcounter = 0
        self.time = 0

    def adjustspeed(self, new_speed):
        self.speed = new_speed

    def unreferance(self):
        SpriteStripAnim.sprite_anims.remove(self)

    def getSpriteAnims(cls):
        return SpriteStripAnim.sprite_anims

    getSpriteAnims = classmethod(getSpriteAnims)
