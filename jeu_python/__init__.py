# Les imports extérieurs
import pygame

# Gère les informations du jeu
import model

# Gère ce qui est affiché
import view

# Gère les contrôles
import controller

import statemanager
import utils
import settings
import userstatistics
import onlineconnector
import pycurl

# Initialisation du module
pygame.init()

# Chargement de l'horloge de pygame
clock = pygame.time.Clock()

# Initialisation de la partie "model" du model/view/controller
model.Model(pygame)

# Intitialisation de la partie "view" du model/view/controller
view.View(pygame)

# Initialisation de la partie "controller" de model/view/controller
controller.Controller(pygame, view)

running = True

# Limite à 60 fps ou à la valeur en config si elle est valide
fps = utils.GameSettings().setfps()

# On charge le mode DEBUG pour les développeurs
settings.DEBUG = True if settings.SettingsManager().readjson()["debug"] is not None and \
                         settings.SettingsManager().readjson()["debug"] is True else False

if settings.DEBUG:
    print("[DEBUG] Debug mode is enabled.")
    print("[DEBUG] (__init__ > l.46) FPS: " + str(fps))

# Chargement des statistiques (local)
userstatistics.UserStatistics().load()

# Chargement du compte de l'utilisateur en ligne (Statistiques distants)
occlass = onlineconnector.OnlineConnector(None, None, False)
try:
    occlass.connect()
    occlass.loadstatistiques()
except pycurl.error:
    pass
except BaseException:
    pass

passed = 0

while running:

    # Les événements:
    running = controller.Controller.checkevents()  # vérifie les interactions pour peut être modifier des infos du model

    if running:
        model.Model.updatemodel(passed)  # Mis à jour des infos du model
        view.View.updatescreen()  # Affichage de tout

        statemanager.StateManager.setstatetime(passed)

        # Limite à 60 fps ou à la valeur en config si elle est valide
        # La syntaxe est une syntaxe dite "ternaire", "si then else alors". Equivant à "cdt ? then : else"
        passed = clock.tick(fps)

# Quitte le module
pygame.quit()
