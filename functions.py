import constantes

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
    i = 1; #i correspond au numéro du bouton
    for boutons in ["Jouer (1 joueur)", "Jouer (2 joueurs)", "Statistiques", "Paramètres"]:
        """Param : screen, color, (x,y,width,height), thickness"""
        """Note La formule de calcul est CANCER xDD"""
        pygame.draw.rect(screen, (192, 192, 192), [80, (30+(i-1)*(30+50)), 480, 50], 0)
        Texte = pygame.font.SysFont('Arial', 25)
        screen.blit(Texte.render(str(boutons), True, (0, 0, 0)), (195, ( i*30+50*(i-1)+(2/50) )))
        i+=1
    pygame.display.flip()

"""Fonction appeler lorsque l'on fait un clique avec l'un des trois boutons de la souris"""
def click_souris(coords, button):
    x = coords[0]
    y = coords[1]
    if x >= 80 and x <= (480+80):
        """
        On clique sur un bouton du menu, ou du moins à l'endroit ou il doit y avoir les bouton du menu principal
        Par la suite, il faudra vérifier si on est dans le menu principal ou pas !!!
        """
        if y >= 30 and y <= (50+30):
            print("Clique sur le premier bouton (Jouer 1 joueur)")
        elif y >= 110 and y <= (50+110):
            print("Clique sur le deuxième bouton (Jouer 2 joueurs)")
        elif y >= 190 and y <= (50+190):
            print("Clique sur le troisème bouton (Statistiques)")
        elif y >= 270 and y <= (50+270):
            print("Clique sur le quatrième bouton (Paramètres)")

def click_clavier(event):
    print('== > Evenement : ', event.type)
    for k,v in event.dict.items():
        print(k,v)
    print()
