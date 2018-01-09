import toolbox
import functions as f


class View:
    def __init__(self):
        print("setup view")

    def mousebutton1down(self, position):  # click gauche
        boutons = toolbox.Button.getButtons(self)
        for bouton in boutons:
            bouton.mousein = f.checkmousebouton(position, bouton.x, bouton.y, bouton.width, bouton.height)

    def mousebutton1up(self, position):
        print("plus en train de click")

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
