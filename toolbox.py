import functions as f

from threading import Thread

boutons = []

class Button:
    """
    La méthode constructeur
    """

    """
    Créer des boutons facilement
    <p>
    :param pygame - PyGame
    :param name - Le texte dans le bouton
    :param surface_bouton - La surface ou seront les boutons
    :param posx - La position x du bouton (par rapport à la gauche)
    :param posy - La position y du bouton (par rapport au haut)
    :param width - La largeur du bouton
    :param height - La hauteur du bouton
    :param couleur_bouton - La couleur du bouton
    :param bordersize - La taille de la bordure (si c'est 0 c'est rempli)
    :param couleur_texte - La couleur du texte
    :param font - Le font du texte
    :param font_size -La taille du font
    :param centeredx - Le texte est-il centré sur l'axe x ?
    :param centeredy - Le texte est-il centré sur l'axe y ?
    :param offset - Le nombre de pixels de décalage par rapport à sa position normale
    """
    def __init__(self, pygame, name, surface_bouton, posx, posy, width, height, couleur_bouton, bordersize, couleur_text, font, font_size, centeredx, centeredy, offset):
        pygame.draw.rect(surface_bouton, couleur_bouton, [posx, posy, width, height], bordersize)
        texte = pygame.font.SysFont(font, font_size)
        if centeredx or centeredy:
            positionx, positiony = f.centretexte(texte.size(name), (width, height))
            if not centeredx:
                positionx = 0
            if not centeredy:
                positiony = 0
        else:
            positionx, positiony = 0, 0

        surface_bouton.blit(texte.render(str(name), True, couleur_text),(positionx + offset, posy + positiony))

        self.x = posx
        self.y = posy
        self.width = width
        self.height = height
        self.text = name

        global boutons
        boutons.append(self)

    def Tween(self, posx, posy, width, height, duration): # transition linéaire
        print()

    def destroy(self):
        print()

    def clicked(self):
        print()

class RunGame(Thread):

    def __init__(self, pygame, screen, ImageMenu, time, viewthread):
        Thread.__init__(self)
        self.pygame = pygame
        self.screen = screen
        self.ImageMenu = ImageMenu
        self.time = time
        self.viewthread = viewthread

    def run(self):
        f.drawstarting(self.pygame, self.screen, self.ImageMenu, self.time, self.viewthread)
        f.drawmenu(self.pygame, self.screen)
