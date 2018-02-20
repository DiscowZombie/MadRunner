# Les imports extérieurs
import pygame
# Utilitaires
import functions
# Gère les informations du jeu
import model
# Gère ce qui est affiché
import view
# Gère les contrôles
import controller
# Les options
import settings
# l'état du jeu
import statemanager
import utils

# On initialise le module
pygame.init()

# On charge l'horloge de pygame
clock = pygame.time.Clock()

# initialisation de la partie "model" du model/view/controller
model.Model(pygame)

# intitialisation de la partie "view" du model/view/controller
view.View(pygame)

# initialisation de la partie "controller" de model/view/controller
controller.Controller(pygame, view)

running = True

# On limite à 60 fps ou à la valeur en config si elle est valide
fps = utils.GameSettings().setfps()
print("[DEBUG] FPS: " + str(fps)) #TODO

passed = 0

while running:
    # Les events:

    running = controller.Controller.checkevents()  # vérifie les interactions pour peut être modifier des infos du model

    if running:
        view.View.updatescreen(passed)  # puis on update tout ça
        statemanager.StateManager.setstatetime(passed)

        # On limite à 60 fps ou à la valeur en config si elle est valide
        # La syntaxe est une syntaxe dite "ternaire", "si then else alors". Equivant à "cdt ? then : else"
        passed = clock.tick(fps)

# On quitte le module
pygame.quit()
