import pygame

#On itialise le module
pygame.init()

#On charge une fenetre de 400 par 300
screen = pygame.display.set_mode((400, 300))

#On charge l'horloge de pygame
clock = pygame.time.Clock()


run = True

#Tant que le jeu tourne
while run:
    #Les events:
    for event in pygame.event.get():
        #Si on appuie sur la croix pour fermer le programme
        if event.type == pygame.QUIT:
            run = False

    #On desine un rectange rouge
    rect = pygame.draw.rect(screen, (255,0,0),  pygame.Rect(100, 200, 100, 100))

    #<-> Mettre la logique du programme <->

    #<-> Fin de la logique <->

    #On met à jour l'écran
    pygame.display.flip()
    #On limite à 60 fps
    clock.tick(60)

#On quitte le module
pygame.quit()
