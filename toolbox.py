import functions as f


class Button:
    """
    La méthode constructeur
    """

    def __init__(self):
        print()

    """
    Créer des boutons facilement
    <p>
    :param pygame - PyGame
    :param name - Le texte dans le bouton
    :param surface_bouton - La surface ou seront les boutons
    :param couleur - La couleur du bouton
    :param couleur_texte - La couleur du texte
    :param bouton_id - Le numéro du bouton
    :param font_size - La taille du font du texte
    :param centeredx - Le texte est-il centré sur l'axe x ?
    :param centeredy - Le texte est-il centré sur l'axe y ?
    :param offset - Le nombre de pixels de décalage par rapport à sa position normale
    """

    def createonmainwindow(self, pygame, name, surface_bouton, couleur_bouton, couleur_text, bouton_id, font_size,
                           centeredx, centeredy, offset):
        pygame.draw.rect(surface_bouton, couleur_bouton, [0, 75 * bouton_id, 400, 50], 0)
        texte = pygame.font.SysFont('Arial', font_size)
        if centeredx or centeredy:
            positionx, positiony = f.centretexte(texte.size(name), (400, 50))
            if not centeredx:
                positionx = 0
            if not centeredy:
                positiony = 0
        else:
            positionx, positiony = 0, 0

        surface_bouton.blit(texte.render(str(name), True, couleur_text),
                            (positionx + offset, 75 * bouton_id + positiony))

    @staticmethod
    def create(pygame, name, surface_bouton, couleur_bouton, couleur_text):
        pygame.draw.rect(surface_bouton, couleur_bouton, [0, 75, 400, 50], 0)
        texte = pygame.font.SysFont('Arial', 25)
        positionx, positiony = f.centretexte(texte.size(name), (400, 50))
        surface_bouton.blit(texte.render(str(name), True, couleur_text), (positionx, 75 + positiony))
