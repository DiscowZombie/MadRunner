# Les couleurs
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 128, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (40, 180, 230)
DARKBLUE = (0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)
GRAY = (192, 192, 192)
PALE = (225, 225, 225)
YELLOW = (255, 255, 0)
DARKYELLOW = (127, 127, 0)
LIGHT_GRAY = (211, 211, 211)

# Pour les requetes web (curl)
WEBSITE_URI = "http://madrunner.discowzombie.fr/"

# l'alphabet :p
ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z"]

# informations sur différents spritesheet
Animations = {
    "gros": {
        "run": {
            "image": "assets/img/personnages/gros/cour.png",
            "framesize": (80, 98),  # taille x et y d'une image du sprite
            "nbimage": 10,
            "initspeed": 20,  # initspeed désigne la vitesse initiale de l'animation (en image par seconde)
            "repeatimage": 1,  # permet de répéter l'image non pas depuis le début, mais depuis une certaine frame
        },
        "jump": {
            "image": "assets/img/personnages/gros/saut.png",
            "framesize": (87, 112),
            "nbimage": 13,
            "initspeed": 60,
            "repeatimage": 10
        },
        "idle": {
            "image": "assets/img/personnages/gros/idle.png",
            "framesize": (80, 98),
            "nbimage": 1,
            "initspeed": 1,
            "repeatimage": 1
        }
    },
    "normal": {
        "run": {
            "image": "assets/img/personnages/normal/cour.png",
            "framesize": (80, 98),
            "nbimage": 10,
            "initspeed": 25,
            "repeatimage": 1
        },
        "jump": {
            "image": "assets/img/personnages/normal/saut.png",
            "framesize": (80, 98),
            "nbimage": 8,
            "initspeed": 60,
            "repeatimage": 5
        },
        "idle": {
            "image": "assets/img/personnages/normal/idle.png",
            "framesize": (80, 98),
            "nbimage": 1,
            "initspeed": 1,
            "repeatimage": 1
        }
    },
    "athlete": {
        "run": {
            "image": "assets/img/personnages/athlete/cour.png",
            "framesize": (80, 98),
            "nbimage": 8,
            "initspeed": 30,
            "repeatimage": 1
        },
        "jump": {
            "image": "assets/img/personnages/athlete/saut.png",
            "framesize": (80, 98),
            "nbimage": 13,
            "initspeed": 60,
            "repeatimage": 11
        },
        "idle": {
            "image": "assets/img/personnages/athlete/idle.png",
            "framesize": (80, 98),
            "nbimage": 1,
            "initspeed": 1,
            "repeatimage": 1
        }
    },
    "poursuiveur": {
        "run": {
            "image": "assets/img/personnages/poursuiveur/cour.png",
            "framesize": (80, 98),
            "nbimage": 10,
            "initspeed": 30,
            "repeatimage": 1
        },
        "jump": {
            "image": "assets/img/personnages/poursuiveur/saut.png",
            "framesize": (80, 98),
            "nbimage": 8,
            "initspeed": 60,
            "repeatimage": 6
        },
        "idle": {
            "image": "assets/img/personnages/poursuiveur/idle.png",
            "framesize": (80, 98),
            "nbimage": 1,
            "initspeed": 1,
            "repeatimage": 1
        }
    }
}

CharactersFeatures = {
    "gros": {
        "image": "assets\img\personnages\gros\idle.png",
        "initspeed": 3,  # la vitesse à laquelle court le personnage à l'état initial, en m/s
        "initenergy": 80  # la quantité d'énergie initiale du personnage (et maximale)
    },
    "normal": {
        "image": "assets/img/personnages/normal/idle.png",
        "initspeed": 4,
        "initenergy": 100
    },
    "athlete": {
        "image": "assets/img/personnages/athlete/idle.png",
        "initspeed": 5,
        "initenergy": 130
    }
}
