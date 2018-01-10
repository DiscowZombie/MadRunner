import functions as f
import view
import controller
import constantes
import pygame

from threading import Thread

class RunGame(Thread):
    def __init__(self, pygame, screen, ImageMenu, time):
        Thread.__init__(self)
        self.pygame = pygame
        self.screen = screen
        self.ImageMenu = ImageMenu
        self.time = time

    def run(self):
        f.drawstarting(self.pygame, self.screen, self.ImageMenu, self.time)
        view.View.drawmainmenu()

""""""""""""""""""""""""
""" GERE LES BOUTONS """
""""""""""""""""""""""""
class Button(object):
    boutons = []

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

    def __init__(self, pygame, name, surface_bouton, surface_position, posx, posy, width, height, couleur_bouton,
                 bordersize, couleur_text, font, font_size, centeredx, centeredy, offset):
        view.View.createbouton(pygame, name, surface_bouton, surface_position, posx, posy, width, height,
                               couleur_bouton,
                               bordersize, couleur_text, font, font_size, centeredx, centeredy, offset)

        self.x = surface_position[0] + posx
        self.y = surface_position[1] + posy
        self.width = width
        self.height = height
        self.text = name
        self.ismousein = False
        self.clicking = False

        Button.boutons.append(self)

    def __del__(self):
        if self in Button.boutons:
            Button.boutons.remove(self) # on l'enlève de nos tables de boutons avant de le détruire
        del self

    def tween(self, posx, posy, width, height, duration):  # transition linéaire
        print()

    def getButtons(cls):
        return Button.boutons

    def getmousein(self):
        return self.ismousein

    def setmousein(self, isin):
        self.ismousein = isin
        if isin:
            # vérifie si on est en train de cliquer dessus
            if controller.Controller.getpressingbuttons()["Mouse1"]:
                self.button1down()

    getButtons = classmethod(getButtons)
    mousein = property(getmousein, setmousein)


class BJouer(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self): # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        view.View.drawmenu() # on dessine le menu par dessus

        POSITION_SURFACE = (120,165)
        TAILLE_SURFACE = [400,150]
        surfacetrans = pygame.Surface(TAILLE_SURFACE, pygame.SRCALPHA,
                                  32)  # La surface où on va mettre les boutons (pour les positionner plus facilement par la suite)
        surfacetrans = surfacetrans.convert_alpha()  # Il faut cependant que la surface a un arrière plan transparent

        POSX = 0
        POSY = 0
        WIDTH = 400
        HEIGHT = 50

        B1Joueur(pygame, "1 joueur", surfacetrans, POSITION_SURFACE, POSX, POSY, WIDTH, HEIGHT, constantes.GRAY, 0,
                       constantes.BLACK, "Arial", 24, True, True, 0)
        POSY += 75
        B2Joueurs(pygame, "2 joueurs", surfacetrans, POSITION_SURFACE, POSX, POSY, WIDTH, HEIGHT, constantes.GRAY, 0,
                       constantes.BLACK, "Arial", 24, True, True, 0)

        view.View.drawreturn()

        view.View.screen.blit(surfacetrans, POSITION_SURFACE)

        pygame.display.update()

class BParam(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self): # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        view.View.drawmenu()

class BStats(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self): # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        view.View.drawmenu()

class B1Joueur(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self): # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        view.View.drawmenu()

class B2Joueurs(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self): # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        view.View.drawmenu()

class BRetour(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self): # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        view.View.drawmenu()
        view.View.drawmainmenu()
