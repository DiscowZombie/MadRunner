import functions
import uielements.image as image
import statemanager
import coregame.spritesheet as sprit
import constantes

# "../assets/img/personnages/gros/cour.png"
st = sprit.SpriteSheet(constantes.SPRITESHEET_PATH).load(10)
ssa = sprit.SpriteStripAnim(st)

"""
Ne fonctionne pour piur 60 fps pour le moment
"""


def loop(pygame):
    # Le perso doit bouger à 15 fps
    for i in range(0, 60 // 4):
        ssa.next(100, 100)
        pygame.time.wait(33)


class CoreGame:

    def __init__(self):
        functions.delete_menu_obj()
        for img in list(image.Image.getImages()):
            img.__del__()
        statemanager.StateManager.setstate(statemanager.StateEnum.PLAYING)
