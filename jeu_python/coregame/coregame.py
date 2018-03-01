import functions
import uielements.image as image
import statemanager
import coregame.spritesheet as sprit
import constantes
import view as v
import mapscripts.jeuxolympiques as jo

"""
Ne fonctionne pour piur 60 fps pour le moment
"""


class Character:

    def __init__(self, characterinfos, posx, posy, scalex, scaley):
        for spritename in characterinfos:
            self.__setattr__(spritename + "sprite", sprit.SpriteStripAnim(characterinfos[spritename], posx, posy, scalex, scaley))
        self.characterinfos = characterinfos
        self.y = 100  # position arbitraire pour l'instant, permet de dessiner le personnage dans un axe y correct (en effet, quand le personnage saute, sa position dans l'axe y va changer !)
        self.distance = 0  # la distance parcouru
        self.state = "run"
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

    characters_sprite = []
    carte = None
    modejeu = None
    level = None
    mapscript = None

    def __init__(self, carte, modejeu, level):
        functions.delete_menu_obj()
        for img in list(image.Image.getImages()):
            img.__del__()
        statemanager.StateManager.setstate(statemanager.StateEnum.PLAYING)

        self.carte = carte
        self.modejeu = modejeu
        self.level = level
        self.time = 0  # temps en ms depuis lequel le jeu a commencé (le chrono)

        # On charge le haut (Texte indicatifs + Bouton "Pause")
        # TODO: Le texte sera créé plus tard quand les variables auront une signification

        # Chargement de la piste
        # Mis en place de la piste
        REPERTOIRE = "assets/img/decors/" + carte + "/piste.png"
        LARGEUR = 0
        HAUTEUR = 175
        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0.35
        SCALE_WIDTH = 1
        SCALE_HEIGHT = 0
        COULEUR = constantes.WHITE
        BORDURE = 0

        piste = image.Image(REPERTOIRE, v.View.screen, POSITION_X,
                            POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        # On dessine le hors piste, d'abord en haut de la piste puis en bas
        """v.View.screen.referance.fill((127, 221, 76), (0, 187, 640, 27))
        v.View.screen.referance.fill((127, 221, 76), (0, 317, 640, 53))"""

        # Initialisation de la carte (IL FAUT TENIR COMPTE DE LA CARTE CHOISI !!)
        if carte == "jeux_olympiques":
            CoreGame.mapscript = jo

        CoreGame.mapscript.init()

        POSITION_X = 0
        POSITION_Y = 65
        SCALE_X = 0.85
        SCALE_Y = 0.35

        CoreGame.characters_sprite.append(Character(constantes.Animations["gros"], POSITION_X, POSITION_Y, SCALE_X, SCALE_Y))  # plus tard dans le développement du jeu, on devra  selectionner le sprite qui convient !

    def loop(cls):  # update l'arrière plan + chaque personnage

        CoreGame.mapscript.refresh()

        for character in CoreGame.characters_sprite:
            new_state = None
            characterinfos = character.characterinfos
            if character.running:
                new_state = "run"
            elif character.jumping:
                new_state = "jump"

            character.state = new_state
            # On charge le perso
            character.__getattribute__(new_state + "sprite").next(-int(characterinfos[new_state]["framesize"][0]/2), -int(characterinfos[new_state]["framesize"][1]/2))


    def spacepressed(cls):
        CoreGame.characters_sprite[0].jump()  # bon, ici on va faire sauter le joueur 1 ! Il faudra pendre en compte cela lors qu'on dera le mode 2 joueurs

    loop = classmethod(loop)
    spacepressed = classmethod(spacepressed)
