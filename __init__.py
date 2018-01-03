#Les imports extérieur
import pygame
from pygame.locals import *
import time
#Nos imports interieur
import functions

#On itialise le module
pygame.init()

#On charge une fenetre de 640 par 480
screen = pygame.display.set_mode((640, 480))
screen.fill((255, 255, 255))
pygame.display.set_caption("MadRunner")

ImageMenu = pygame.image.load("assets/img/menu_fond.png").convert_alpha()
pygame.display.set_icon(ImageMenu) # Icone du jeu

#On charge l'horloge de pygame
clock = pygame.time.Clock()

functions.drawstarting(pygame, ImageMenu, screen, time)
functions.drawmenu(pygame, screen)

run = True

#Tant que le jeu tourne
while run:
    #Les events:
    for event in pygame.event.get():
        #Si on appuie sur la croix pour fermer le programme
        if event.type == pygame.QUIT:
            run = False

    #<-> Mettre la logique du programme <->

    #<-> Fin de la logique <->

    #On met à jour l'écran
    pygame.display.flip()
    #On limite à 60 fps
    clock.tick(60)

#On quitte le module
pygame.quit()
