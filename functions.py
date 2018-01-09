import constantes
import toolbox


def centretexte(textsize, espace):  # Utilitaire pour center un texte ! Retourne la position x et y du texte
    return int(espace[0] / 2 - textsize[0] / 2), int(espace[1] / 2 - textsize[1] / 2)


def checkmousebouton(mousepos, buttonx, buttony, buttonwidth,
                     buttonheight):  # Utilitaire pour savoir si la souris se trouve dedans un bouton
    posx, posy = mousepos[0], mousepos[1]
    minx, maxx = buttonx, buttonx + buttonwidth
    miny, maxy = buttony, buttony + buttonheight
    if posx >= minx and posx <= maxx and posy >= miny and posy <= maxy:
        return True
    return False


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
        pygame.display.update()  # acutalise ce qui doit etre affichee

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
    POSITION_SURFACE = (120, 150)
    TAILLE_SURFACE = [400, 200]
    surfacetrans = pygame.Surface(TAILLE_SURFACE, pygame.SRCALPHA,
                                  32)  # La surface où on va mettre les boutons (pour les positionner plus facilement par la suite)
    surfacetrans = surfacetrans.convert_alpha()  # Il faut cependant que la surface a un arrière plan transparent

    POSX = 0
    POSY = 0
    WIDTH = 400
    HEIGHT = 50

    toolbox.BJouer(pygame, "Jouer", surfacetrans, POSITION_SURFACE, POSX, POSY, WIDTH, HEIGHT, constantes.GRAY, 0,
                       constantes.BLACK, "Arial", 24, True, True, 0)
    POSY += 75
    toolbox.BStats(pygame, "Statistiques", surfacetrans, POSITION_SURFACE, POSX, POSY, WIDTH, HEIGHT, constantes.GRAY, 0,
                       constantes.BLACK, "Arial", 24, True, True, 0)
    POSY += 75
    toolbox.BParam(pygame, "Paramètres", surfacetrans, POSITION_SURFACE, POSX, POSY, WIDTH, HEIGHT, constantes.GRAY, 0,
                       constantes.BLACK, "Arial", 24, True, True, 0)

    screen.blit(surfacetrans, POSITION_SURFACE)
    # RAPPELS:
    # position x des boutons: 120 à 520
    # position y: jouer: 150 à 200 , statistiques: 225 à 275 , paramètres: 300 à 350
    pygame.display.update()


def click_clavier(event):
    print('== > Evenement : ', event.type)
    for k, v in event.dict.items():
        print(k, v)
    print()


def isvalidint(supposedint):
    var = True if (supposedint is not None and int(supposedint) is not None) else False
    return var
