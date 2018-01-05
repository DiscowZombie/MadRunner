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
    """
    def createOnMainWindow(self, pygame, name, surface_bouton, couleur_bouton, couleur_text, bouton_id):
        pygame.draw.rect(surface_bouton, couleur_bouton, [0, 75 * bouton_id, 400, 50], 0)
        texte = pygame.font.SysFont('Arial', 25)
        positionx, positiony = f.CentreTexte(texte.size(name), (400, 50))
        surface_bouton.blit(texte.render(str(name), True, couleur_text), (positionx, 75 * bouton_id + positiony))
