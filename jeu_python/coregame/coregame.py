import functions
import uielements.image as image
import statemanager
import coregame.spritesheet as sprit
import constantes

"""
Ne fonctionne pour piur 60 fps pour le moment
"""


class CoreGame:

    character_sprite = None

    def __init__(self):
        functions.delete_menu_obj()
        for img in list(image.Image.getImages()):
            img.__del__()
        statemanager.StateManager.setstate(statemanager.StateEnum.PLAYING)

        CoreGame.character_sprite = sprit.SpriteStripAnim(constantes.Animations["cour"]["gros"])

    def loop(cls):
        # Le perso doit bouger à 15 fps
        #for i in range(0, 60 // 4):
        CoreGame.character_sprite.next(100, 100)

    loop = classmethod(loop)
