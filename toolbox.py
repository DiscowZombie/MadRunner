import functions as f
import view
import controller

from threading import Thread


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

    def tween(self, posx, posy, width, height, duration):  # transition linéaire
        print()

    def destroy(self):
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
        print("vous avez cliquer sur moi !! JOUER MAINTENANT")


class BParam(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self): # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        print("vous avez cliquer sur moi !! PARAMETRES MAINTENANT")

class BStats(Button):
    def __init__(*arguments):
        Button.__init__(*arguments)

    def button1down(self): # on défini une specilisation de ce bouton ! cette fonction est executé lorsqu'on clique sur ce bouton
        print("vous avez cliquer sur moi !! STATISTIQUES MAINTENANT")


class RunGame(Thread):
    def __init__(self, pygame, screen, ImageMenu, time):
        Thread.__init__(self)
        self.pygame = pygame
        self.screen = screen
        self.ImageMenu = ImageMenu
        self.time = time

    def run(self):
        f.drawstarting(self.pygame, self.screen, self.ImageMenu, self.time)
        f.drawmenu(self.pygame, self.screen)
