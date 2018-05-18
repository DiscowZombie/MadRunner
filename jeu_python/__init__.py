# Les imports extérieurs
import pygame

# Gère les informations du jeu
import model

# Gère ce qui est affiché
import view

# Gère les contrôles
import controller

import functions
import statemanager
import settings
import userstatistics
import onlineconnector
import pycurl

# Initialisation du mixer de pygame (pour les sons)
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# Initialisation de pygame
pygame.init()

# Initialisation du font
pygame.font.init()

# Chargement de l'horloge de pygame
clock = pygame.time.Clock()

# Initialisation de la partie "model" du model/view/controller
model.Model()  # bon, en réalité, il n'y a rien à initialiser ici...

# Intitialisation de la partie "view" du model/view/controller
view.View()

# Initialisation de la partie "controller" de model/view/controller
controller.Controller()  # rien à initialiser ici aussi...

# Chargement des paramètres du joueur
settings.SettingsManager()

# Limite à 60 fps ou à la valeur en config si elle est valide
fps = functions.setfps()

# On charge le mode DEBUG pour les développeurs
current_settings = settings.SettingsManager.current_settings
settings.DEBUG = True if current_settings["debug"] is not None and \
                         current_settings["debug"] is True else False

if settings.DEBUG:
    print("[DEBUG] Debug mode is enabled.")
    print("[DEBUG] (__init__ > l.46) FPS: " + str(fps))

# Chargement des statistiques (local)
userstatistics.UserStatistics().load()

# Chargement du compte de l'utilisateur en ligne (Statistiques distants)
occlass = onlineconnector.OnlineConnector(None, None, False)
try:
    occlass.connect()
except pycurl.error:
    pass
except BaseException:
    pass

try:
    occlass.loadstatistiques()
except BaseException:
    pass

passed = 0
running = True

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
