import pygame
import model
import view


class Controller:
    pressing_buttons = {}

    def __init__(self):
        self.initialised = True

    @classmethod
    def checkevents(cls):
        for event in pygame.event.get():
            # Si on appuie sur la croix pour fermer le programme
            if event.type == pygame.QUIT:
                return False
            # si on redimensionne la fenêtre
            elif event.type == pygame.VIDEORESIZE:
                view.View.updatewindow(event.size)
            # clic sur la souris
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
                    model.Model.mousebutton1down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                button_number = event.button
                Controller.pressing_buttons["Mouse" + str(button_number)] = False
                if button_number == 1:  # clic gauche
                    model.Model.mousebutton1up()
            elif event.type == pygame.MOUSEMOTION:
                model.Model.mousebutton1move(event.pos)
            elif event.type == pygame.KEYDOWN:
                model.Model.keydown(event)
        return True

    @classmethod
    def getpressingbuttons(cls):
        return Controller.pressing_buttons
