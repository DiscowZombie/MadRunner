# Les couleurs
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DARKBLUE = (0,0,128)
WHITE = (255,255,255)
BLACK = (0,0,0)
PINK = (255,200,200)
GRAY = (192, 192, 192)

# Pour les chemins d'accès
CONFIG_PATH = "config/"

# informations sur différents spritesheet
Animations = {
    "cour": {
        "gros": {
            "image": "assets/img/personnages/gros/cour.png",
            "nbimage": 10,
            "initspeed": 20  # initspeed désigne la vitesse initiale de l'animation (en image par seconde)
        },
        "normal": {
            "image": "",
            "nbimage": 0
        },
        "athlete": {
            "image": "",
            "nbimage": 0
        }
    },
    "saut": {
        "gros": {
            "image": "",
            "nbimage": 0
        },
        "normal": {
            "image": "",
            "nbimage": 0
        },
        "athlete": {
            "image": "",
            "nbimage": 0
        }
    }
}
