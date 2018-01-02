"""On déssine la belle apparition du logo"""
def drawstarting():
    #Le bel effet d'apparition
    for i in range(1, 101):
        Surface = pygame.Surface((200,200)) # la surface ou on va mettre le titre du jeu et l'image du jeu
        Surface.fill((255,255,255))
        Surface.set_alpha(int(2.55*i)) # alpha finale: 255 (opaque)

        Texte = pygame.font.SysFont("arial", int(0.44*i)) # taille finale du font: 44
        SurfaceTexte = Texte.render("Mad Runner", True, (0,0,0))
        Surface.blit(SurfaceTexte,(100 - i,0)) # position finale: 0 sur 0

        Icone = pygame.transform.scale(ImageMenu,(2*i,int(1.2*i))) # taille finale: 200 sur 120
        Surface.blit(Icone,(100 - i,140 - int(0.6*i))) # position finale: 0 sur 80

        screen.blit(Surface,(220,120)) # position finale: 220 sur 120
        pygame.display.flip() # acutalise ce qui doit etre affichee

import pygame

#On itialise le module
pygame.init()

#On charge une fenetre de 400 par 300
screen = pygame.display.set_mode((640, 480))
screen.fill((255, 255, 255))
pygame.display.set_caption("MadRunner")

ImageMenu = pygame.image.load("menu_fond.png").convert_alpha()
pygame.display.set_icon(ImageMenu) # Icone du jeu

#On charge l'horloge de pygame
clock = pygame.time.Clock()

drawstarting()

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
