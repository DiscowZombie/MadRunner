# Les imports extérieurs
import pygame
from pygame.locals import *
import time
# Nos imports interieur
import functions
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

gamethread = toolbox.RunGame(pygame, screen, ImageMenu, time)
gamethread.start()

run = True

# Tant que le jeu tourne
while run:
    # Les events:
    for event in pygame.event.get():
        # Si on appuie sur la croix pour fermer le programme
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            functions.click_souris(event.dict['pos'], event.dict['button'])
        elif event.type == pygame.KEYDOWN:
            functions.click_clavier(event)

    # <-> Mettre la logique du programme <->

    # <-> Fin de la logique <->

    # On met à jour l'écran
    time.sleep(0.01)
    # On limite à 60 fps ou à la valeur en config si elle est valide
    # La syntaxe est une syntaxe dite "ternaire", "si then else alors". Equivant à "cdt ? then : else"
    clock.tick(settings.Settings().getsetting("limit_fps") if functions.isvalidint(settings.Settings().getsetting("limit_fps")) else 60)

# On quitte le module
pygame.quit()
