import pygame
import toolbox
import functions


class Controller:

    def __init__(self):
        self.PressingKeys = []

    def checkevents(self):
        for event in pygame.event.get():
            # Si on appuie sur la croix pour fermer le programme
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # RAPPEL, boutons possible:
                # 1: Clique gauche
                # 2: Clique milieu (scroll)
                # 3: Clique droit
                # 4: Scroll vers le haut
                # 5: Scroll vers le bas
                if event.button == 1:  # clic gauche
                    boutons = toolbox.Button.getButtons(self)
                    mousepos = event.pos
                    for bouton in boutons:
                        IsIn = functions.checkmousebouton(mousepos, bouton.x, bouton.y, bouton.width, bouton.height)
                        if IsIn:
                            print("clic sur bouton avec texte " + bouton.text)

            elif event.type == pygame.KEYDOWN:
                print("ok")
        return True
