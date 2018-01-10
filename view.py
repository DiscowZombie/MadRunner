import toolbox
import functions as f
import constantes

class View:

    pygame = None
    screen = None

    def __init__(self, pygame, screen):
        View.pygame = pygame
        View.screen = screen

    def mousebutton1down(self, position):  # click gauche
        boutons = toolbox.Button.getButtons()
        for bouton in boutons:
            bouton.mousein = f.checkmousebouton(position, bouton.x, bouton.y, bouton.width, bouton.height)

    def mousebutton1up(self, position):
        print("plus en train de click")

    def addcontrollerobject(self, controller):
        self.controller = controller

    def drawmenu(cls):
        fond = View.pygame.image.load("assets/img/background_temporaire.jpg").convert()
        View.screen.blit(fond, (0, 0))
        for bouton in toolbox.Button.getButtons():
            bouton.__del__()# on efface l'objet bouton puisqu'on va l'effacer de l'écran, donc pas besoin de référance vers celui-ci

    def drawreturn(cls):
        POSITION_BOUTON = (0,0)
        TAILLE_BOUTON = [100,50]
        surfacetrans = View.pygame.Surface(TAILLE_BOUTON, View.pygame.SRCALPHA,
                                      32)  # La surface où on va mettre les boutons (pour les positionner plus facilement par la suite)
        surfacetrans = surfacetrans.convert_alpha()  # Il faut cependant que la surface a un arrière plan transparent

        toolbox.BRetour(View.pygame, "Retour", surfacetrans, POSITION_BOUTON, POSITION_BOUTON[0], POSITION_BOUTON[1], TAILLE_BOUTON[0], TAILLE_BOUTON[1], constantes.GRAY, 0,
                       constantes.BLACK, "Arial", 24, True, True, 0)

        View.screen.blit(surfacetrans, POSITION_BOUTON)

    def drawmainmenu(cls):
        View.drawmenu()
        POSITION_SURFACE = (120, 150)
        TAILLE_SURFACE = [400, 200]
        surfacetrans = View.pygame.Surface(TAILLE_SURFACE, View.pygame.SRCALPHA,
                                      32)  # La surface où on va mettre les boutons (pour les positionner plus facilement par la suite)
        surfacetrans = surfacetrans.convert_alpha()  # Il faut cependant que la surface a un arrière plan transparent

        POSX = 0
        POSY = 0
        WIDTH = 400
        HEIGHT = 50

        toolbox.BJouer(View.pygame, "Jouer", surfacetrans, POSITION_SURFACE, POSX, POSY, WIDTH, HEIGHT, constantes.GRAY, 0,
                           constantes.BLACK, "Arial", 24, True, True, 0)
        POSY += 75
        toolbox.BStats(View.pygame, "Statistiques", surfacetrans, POSITION_SURFACE, POSX, POSY, WIDTH, HEIGHT, constantes.GRAY, 0,
                           constantes.BLACK, "Arial", 24, True, True, 0)
        POSY += 75
        toolbox.BParam(View.pygame, "Paramètres", surfacetrans, POSITION_SURFACE, POSX, POSY, WIDTH, HEIGHT, constantes.GRAY, 0,
                           constantes.BLACK, "Arial", 24, True, True, 0)

        View.screen.blit(surfacetrans, POSITION_SURFACE)
        # RAPPELS:
        # position x des boutons: 120 à 520
        # position y: jouer: 150 à 200 , statistiques: 225 à 275 , paramètres: 300 à 350
        View.pygame.display.update()

    drawmenu = classmethod(drawmenu)
    drawmainmenu = classmethod(drawmainmenu)
    drawreturn = classmethod(drawreturn)

    @staticmethod
    def createbouton(pygame, name, surface_bouton, surface_position, posx, posy, width, height, couleur_bouton,
                     bordersize, couleur_text, font, font_size, centeredx, centeredy, offset):
        pygame.draw.rect(surface_bouton, couleur_bouton, [posx, posy, width, height], bordersize)
        texte = pygame.font.SysFont(font, font_size)
        if centeredx or centeredy:
            positionx, positiony = f.centretexte(texte.size(name), (width, height))
            if not centeredx:
                positionx = 0
            if not centeredy:
                positiony = 0
        else:
            positionx, positiony = 0, 0

        surface_bouton.blit(texte.render(str(name), True, couleur_text), (positionx + offset, posy + positiony))
