import pygame
import toolbox
import functions


class Controller:

    pressing_buttons = {}

    def __init__(self,view):
        self.view = view

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
                button_number = event.button
                Controller.pressing_buttons["Mouse" + str(button_number)] = True
                if button_number == 1:  # clic gauche
                    self.view.mousebutton1down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                button_number = event.button
                Controller.pressing_buttons["Mouse" + str(button_number)] = False
                if button_number == 1:  # clic gauche
                    self.view.mousebutton1up(event.pos)

            elif event.type == pygame.KEYDOWN:
                print("ok")
        return True

    def getpressingbuttons(cls):
        return Controller.pressing_buttons

    getpressingbuttons = classmethod(getpressingbuttons)


