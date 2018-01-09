# Les imports extérieurs
import pygame
from pygame.locals import *
import time
# Nos imports interieur
import functions
# Gère les contrôles
import controller
# Gère ce qui est affiché
import view
# Quelques utilitaires
import toolbox
# Les options
import settings

# On initialise le module
pygame.init()

# On charge une fenêtre de 640 par 480
screen = pygame.display.set_mode((640, 480))
screen.fill((255, 255, 255))
pygame.display.set_caption("Mad Runner")

ImageMenu = pygame.image.load("assets/img/menu_fond.png").convert_alpha()
pygame.display.set_icon(ImageMenu) # Icone du jeu

# On charge l'horloge de pygame
clock = pygame.time.Clock()

view = view.View()
controls = controller.Controller(view)
view.addcontrollerobject(controls)

gamethread = toolbox.RunGame(pygame, screen, ImageMenu, time)
gamethread.start()

running = True

while running:
    # Les events:

    running = controls.checkevents()

    time.sleep(0.01)

    # On limite à 60 fps ou à la valeur en config si elle est valide
    # La syntaxe est une syntaxe dite "ternaire", "si then else alors". Equivant à "cdt ? then : else"
    clock.tick(settings.Settings().getsetting("limit_fps") if functions.isvalidint(settings.Settings().getsetting("limit_fps")) else 60)

# On quitte le module
pygame.quit()
