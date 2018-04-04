# Les couleurs
RED = (255,0,0)
GREEN = (0,255,0)
DARKGREEN = (0,128,0)
BLUE = (0,0,255)
DARKBLUE = (0,0,128)
WHITE = (255,255,255)
BLACK = (0,0,0)
PINK = (255,200,200)
GRAY = (192, 192, 192)
YELLOW = (255, 255, 0)
DARKYELLOW = (127, 127, 0)

# Pour les chemins d'accès
CONFIG_PATH = "config/"

# l'alphabet :p
ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

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
        }
    },
    "normal": {
        "run": {
            "image": "",
            "nbimage": 0,
            "initspeed": 20,
            "repeatimage": 1
        } ,
        "jump": {
            "image": "",
            "nbimage": 0,
            "initspeed": 20,
            "repeatimage": 1
        }
    },
    "athlete": {
        "run": {
            "image": "",
            "nbimage": 0,
            "initspeed": 20
        },
        "jump": {
            "image": "",
            "nbimage": 0,
            "initspeed": 20
        }
    }
}

CharactersFeatures = {
    "gros": {
        "initspeed": 3,  # la vitesse à laquelle court le personnage à l'état initial, en m/s
        "initenergy": 100  # la quantité d'énergie initiale du personnage (et maximale)
    }
}
