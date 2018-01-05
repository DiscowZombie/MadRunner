import constantes
import toolbox


def centretexte(textsize, espace):  # Utilitaire pour center un texte ! Retourne la position x et y du texte
    return int(espace[0] / 2 - textsize[0] / 2), int(espace[1] / 2 - textsize[1] / 2)


# On déssine la balle apparition du logo
def drawstarting(pygame, screen, imagemenu, time):
    def drawtitle(i, reverse):  # i va de 0 (debut de l'animation) a 100 (fin de l'animation)
        alpha = None
        if reverse:
            a = pygame.Surface((640, 480))  # une surface
            a.fill((255, 255, 255))
            screen.blit(a, (0, 0))
            alpha = 255 - int(2.55 * i)
            i = 100
        else:
            alpha = int(2.55 * i)

        surface = pygame.Surface((225, 225))  # la surface ou on va mettre le titre du jeu et l'image du jeu
        surface.fill((255, 255, 255))
        surface.set_alpha(alpha)  # alpha finale: 255 (opaque)

        texte = pygame.font.SysFont("arial", int(0.44 * i))  # taille finale du font: 44
        surfacetexte = texte.render("Mad Runner", True, (0, 0, 0))
        surface.blit(surfacetexte, (100 - i, 0))  # position finale: 0 sur 0

        icone = pygame.transform.scale(imagemenu, (2 * i, int(1.2 * i)))  # taille finale: 200 sur 120
        surface.blit(icone, (100 - i, 140 - int(0.6 * i)))  # position finale: 0 sur 80

        screen.blit(surface, (220, 120))  # position finale: 220 sur 120
        pygame.display.flip()  # acutalise ce qui doit etre affichee

    # Le bel effet d'apparition
    for i in range(1, 101):
        drawtitle(i, False)

    time.sleep(2)

    for i in range(1, 101):
        drawtitle(i, True)

    time.sleep(0.5)


# On déssine le menu : Jouer, Statistiques, Paramètres
def drawmenu(pygame, screen):
    fond = pygame.image.load("assets/img/background_temporaire.jpg").convert()
    screen.blit(fond, (0, 0))
    surfacetrans = pygame.Surface([400, 200], pygame.SRCALPHA,
                                  32)  # La surface où on va mettre les boutons (pour les positionner plus facilement par la suite)
    surfacetrans = surfacetrans.convert_alpha()  # Il faut cependant que la surface a un arrière plan transparent

    i = 0
    for bouton in ["Jouer", "Statistiques", "Paramètres"]:
<<<<<<< HEAD
        toolbox.Button().createOnMainWindow(pygame, bouton, SurfaceTrans, constantes.GRAY, constantes.BLACK, i, 24, True, True, 0)
        i+=1
=======
        toolbox.Button().createonmainwindow(pygame, bouton, surfacetrans, constantes.GRAY, constantes.BLACK, i)
        i += 1
>>>>>>> 963e8167634566f3825aa1196c550ca9f520f469

    screen.blit(surfacetrans, (120, 150))
    # RAPPELS:
    # position x des boutons: 120 à 520
    # position y: jouer: 150 à 200 , statistiques: 225 à 275 , paramètres: 300 à 350
    pygame.display.flip()


# Fonction appeler lorsque l'on fait un clique avec l'un des trois boutons de la souris"""
def click_souris(coords, button):
    # RAPPEL, boutons possible:
    # 1: Clique gauche
    # 2: Clique milieu (scroll)
    # 3: Clique droit
    # 4: Scroll vers le haut
    # 5: Scroll vers le bas
    x = coords[0]
    y = coords[1]
    if x >= 80 and x <= 560: # 480 + 80
        """
        On clique sur un bouton du menu, ou du moins à l'endroit ou il doit y avoir les boutons du menu principal
        Par la suite, il faudra vérifier si on est dans le menu principal ou pas !!!
        """
        if x >= 120 and x <= 520:
            if y >= 150 and y <= 200:
                print("Clique sur le premier bouton (Jouer)")
            elif y >= 225 and y <= 275:
                print("Clique sur le deuxième bouton (Statistiques)")
            elif y >= 300 and y <= 350:
                print("Clique sur le troisème bouton (Paramètres)")


def click_clavier(event):
    print('== > Evenement : ', event.type)
    for k, v in event.dict.items():
        print(k, v)
    print()
