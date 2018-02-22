import functions
import uielements.image as image
import statemanager
import coregame.spritesheet as sprit
import constantes

"""
Ne fonctionne pour piur 60 fps pour le moment
"""


class Character:

    def __init__(self, characterinfos, posx, posy):
        for spritename in characterinfos:
            self.__setattr__(spritename + "sprite", sprit.SpriteStripAnim(characterinfos[spritename], posx, posy))
        self.characterinfos = characterinfos
        self.y = 100  # position arbitraire pour l'instant, permet de dessiner le personnage dans un axe y correct (en effet, quand le personnage saute, sa position dans l'ace y va changer !)
        self.distance = 0  # la distance parcouru
        self.running = True  # on va supposer pour l'instant que le gars cour tout de suite, mais plus tard, ce ne sera pas le cas (car on montrera un 3,2,1, go !)
        self.jumping = False  # le personnage est-il en train de sauter ?
        self.energy = 100  # untité arbitraire pour l'instant, permet de savoir la quantité d'énergie restante pour sauter ou courir vite

    def run(self):
        print("rien d'intéressant ici !")  # en effet ! servira plus tard lorqu'on fera le à vos marques pret go !

    def jump(self):
        if not self.jumping and self.energy >= 10:  # unité encore arbitraire pour l'énergie, on verra cela plus tard !
            self.energy += -10
            self.jumping = True
            self.running = False


class CoreGame:

    character_sprite = None

    def __init__(self):
        functions.delete_menu_obj()
        for img in list(image.Image.getImages()):
            img.__del__()
        statemanager.StateManager.setstate(statemanager.StateEnum.PLAYING)

        POSITION_X = 100
        POSITION_Y = 100

        CoreGame.character_sprite = Character(constantes.Animations["gros"], POSITION_X, POSITION_Y)  # plus tard dans le développement du jeu, on devra  selectionner le sprite qui convient !

    def loop(cls):
        state = None
        character = CoreGame.character_sprite
        characterinfos = character.characterinfos
        if character.running:
            state = "run"
        elif character.jumping:
            state = "jump"

        character.__getattribute__(state + "sprite").next(-int(characterinfos[state]["framesize"][0]/2), -int(characterinfos[state]["framesize"][1]/2))

    def spacepressed(cls):
        CoreGame.character_sprite.jump()

    loop = classmethod(loop)
    spacepressed = classmethod(spacepressed)
