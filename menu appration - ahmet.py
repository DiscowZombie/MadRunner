import pygame
import time

pygame.init()

fenetre = pygame.display.set_mode((640, 480)) # on peut mettre "FULLSCREEN" en deuxieme argument pour la mettre en pleine ecran
fenetre.fill((255,255,255))
pygame.display.set_caption("Mad runner") # titre du jeu !
ImageMenu = pygame.image.load("Menu.png").convert_alpha()
pygame.display.set_icon(ImageMenu) # icone du jeu

for i in range(100):
    """on peut utiliser ces 3 lignes pour completement renouveler l'ecran, mais je trouve que ca donnait un resultat moins beau, tu peux essayer"""
    #a = pygame.Surface((640,480)) # une surface
    #a.fill((255,255,255))
    #fenetre.blit(a,(0,0)) # position finale: 220 sur 100

    i = i + 1 # juste pour pas avoir ce foutu 0 et cette foutu boucle qui s'arrete a 99 !
    Surface = pygame.Surface((200,200)) # la surface ou on va mettre le titre du jeu et l'image du jeu
    Surface.fill((255,255,255))
    Surface.set_alpha(int(2.55*i)) # alpha finale: 255 (opaque)

    Texte = pygame.font.SysFont("arial",int(0.44*i)) # taille finale du font: 44
    SurfaceTexte = Texte.render("Mad Runner",True,(0,0,0))
    Surface.blit(SurfaceTexte,(100 - i,0)) # position finale: 0 sur 0

    Icone = pygame.transform.scale(ImageMenu,(2*i,int(1.2*i))) # taille finale: 200 sur 120
    Surface.blit(Icone,(100 - i,140 - int(0.6*i))) # position finale: 0 sur 80

    fenetre.blit(Surface,(220,120)) # position finale: 220 sur 120
    pygame.display.flip() # acutalise ce qui doit etre affichee

    #time.sleep(0.1) # j'utilisait ca pour voir si l'animation etait assez fluide ou pas

continuer = True

while continuer:
    event = pygame.event.wait()
    eventtype = event.type
    if eventtype == pygame.QUIT:
        continuer = False
    elif eventtype == pygame.KEYDOWN:
        if event.key == pygame.K_e:
            print("ok")

pygame.quit()