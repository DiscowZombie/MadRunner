"""On déssine la belle apparition du logo"""
def drawstarting(pygame, ImageMenu, screen, time):
    #Le bel effet d'apparition
    for i in range(1, 101):
        Surface = pygame.Surface((225, 225)) # la surface ou on va mettre le titre du jeu et l'image du jeu
        Surface.fill((255,255,255))
        Surface.set_alpha(int(2.55*i)) # alpha finale: 255 (opaque)

        Texte = pygame.font.SysFont("arial", int(0.44*i)) # taille finale du font: 44
        SurfaceTexte = Texte.render("MadRunner", True, (0, 0, 0))
        Surface.blit(SurfaceTexte,(100 - i, 0)) # position finale: 0 sur 0

        Icone = pygame.transform.scale(ImageMenu,(2*i,int(1.2*i))) # taille finale: 200 sur 120
        Surface.blit(Icone,(100 - i, 140 - int(0.6*i))) # position finale: 0 sur 80

        screen.blit(Surface, (220, 120)) # position finale: 220 sur 120
        pygame.display.flip() # acutalise ce qui doit etre affichee
    time.sleep(2)

"""On déssine le menu : Jouer (1 joueur), Joueur (2 joueurs), Statistiques (+ Paramètres)"""
def drawmenu(pygame, screen):
    fond = pygame.image.load("assets/img/background_temporaire.jpg").convert()
    screen.blit(fond, (0, 0))
    pygame.draw.rect(screen, (255, 255, 0), [80, 30, 430, 70], 1)
    pygame.display.flip()
