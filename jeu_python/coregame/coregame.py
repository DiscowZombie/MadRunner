import functions
from uielements import button as button
from uielements import image as image
from uielements import surface as surface
from uielements import rect as rect
from uielements import text as text
import statemanager
import coregame.spritesheet as sprit
import coregame.gameobjects.key as key
import constantes
import view as v
import mapscripts.jeuxolympiques as jo
import endgame.endgame as eg

import random

"""
Ne fonctionne pour piur 60 fps pour le moment
"""


class Character:

    def __init__(self, characterfeatures, characterinfos, posx, posy, scalex, scaley):
        for spritename in characterinfos:
            self.__setattr__(spritename + "sprite",
                             sprit.SpriteStripAnim(characterinfos[spritename], posx, posy, scalex, scaley))
        self.characterinfos = characterinfos
        self.characterfeatures = characterfeatures
        self.x = posx
        self.y = posy
        self.scalex = scalex
        self.scaley = scaley
        self.state = "run"
        self.running = True  # on va supposer pour l'instant que le gars cour tout de suite, mais plus tard, ce ne sera pas le cas (car on montrera un 3,2,1, go !)
        self.jumping = False  # le personnage est-il en train de sauter ?
        self.energy = characterfeatures["initenergy"]
        self.speed = characterfeatures["initspeed"]

    def run(self):
        self.running = True
        self.jumping = False

    def jump(self):
        if not self.jumping and self.energy >= 10:  # unité encore arbitraire pour l'énergie, on verra cela plus tard !
            self.energy -= 10
            self.speed -= 0.15 * self.speed  # Sauter reduit sa vitesse de 15%
            self.jumping = True
            self.running = False

    def changeState(self, new_state):
        self.state = new_state

    def boost(self, attribut, amount):  # permet d'augmenter la valeur d'un attribut (ou de le diminuer si amount est négatif)
        if attribut == "energy":  # petite exception pour cette attribut qui ne peut excéder la quantité d'énergie initiale
            max_energy = self.characterfeatures["initenergy"]
            if self.energy + amount > max_energy:
                amount = max_energy - self.energy
        if self.__getattribute__(attribut) + amount < 0:  # pour empêcher d'avoir de valeurs négatives !
            amount = -self.__getattribute__(attribut)
        self.__setattr__(attribut, self.__getattribute__(attribut) + amount)


class CoreGame:
    characters_sprite = []
    carte = None
    modejeu = None
    level = None
    mapscript = None

    pause = False
    time = 0  # temps en ms depuis lequel le jeu a commencé (le chrono)
    distance = 0  # la distance parcouru
    finished = False  # la course est-elle finie ?

    surface_boutons = None  # la surface sur laquelle les boutons à appuyer sont dessinés

    vitesseobj = None  # le texte sur lequel on écrit la vitesse du courreur
    tempsobj = None  # le texte sur lequel on écrit le temps de la course (AFFICHé SEULEMENT EN 400M ET 400M HAIE)
    distanceobj = None  # le texte sur lequel on écrit la distance parcouru (AFFICHé SEULEMENT EN COURSE INFINI)
    lignearriveobj = None  # la surface qui fait office de ligne d'arrivé (n'existe que lorqu'on est assez proche de l'arrivé)

    # La barre d'énergie
    barre_energie_in = None
    barre_energie_out = None

    # On stoque la piste pour pouvoir l'enlever à la fin
    piste = None

    def __init__(self, carte, modejeu, level):

        """
        :param carte - Valeurs possibles: Jeux Olympiques, Athènes, Forêt
        :param modejeu - Valeurs possibles: 400m, 400m haie, Course infinie
        :param level - Valeurs possibles: Facile, Moyen, Difficile
        """

        functions.delete_menu_obj()
        for img in list(image.Image.getImages()):
            img.unreferance()
        statemanager.StateManager.setstate(statemanager.StateEnum.PLAYING)

        self.carte = carte
        self.modejeu = modejeu
        self.level = level
        self.time = 0
        self.distance = 0
        self.keys = []
        self.availablekeys = list(constantes.ALPHABET)

        CoreGame.modejeu = modejeu

        # Création de la barre d'énergie
        # la bordure
        LARGEUR = 0
        HAUTEUR = 0
        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0.2
        SCALE_Y = 0.005
        SCALE_WIDTH = 0.4
        SCALE_HEIGHT = 0.04
        COULEUR = constantes.DARKYELLOW
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = False

        CoreGame.barre_energie_out = surface.Surface(ALPHA, CONVERT_ALPHA, v.View.screen, POSITION_X, POSITION_Y,
                                                     SCALE_X, SCALE_Y, LARGEUR,
                                                     HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                                     BORDURE)

        # l'intérieur (en tant qu'objet rect, et non en tant qu'objet surface)
        LARGEUR = -4
        HAUTEUR = -4
        POSITION_X = 2
        POSITION_Y = 2
        SCALE_X = 0
        SCALE_Y = 0
        SCALE_WIDTH = 1
        SCALE_HEIGHT = 1
        COULEUR = constantes.GREEN
        BORDURE = 0  # rempli

        CoreGame.barre_energie_in = rect.Rect(CoreGame.barre_energie_out, POSITION_X, POSITION_Y, SCALE_X,
                                              SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                              BORDURE)

        # Création du texte qui affiche la vitesse
        TEXTE = ""
        ANTIALIAS = True
        COULEUR = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 20
        CENTRE_X = False
        CENTRE_Y = True
        ARRIERE_PLAN = constantes.WHITE
        ECART = 3
        SEUL = True
        LARGEUR = 0
        HAUTEUR = 0
        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        SCALE_WIDTH = 0.2
        SCALE_HEIGHT = 0.05
        COULEUR_ARRIERE = constantes.WHITE
        BORDURE = 0

        CoreGame.vitesseobj = text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                                        ECART, SEUL,
                                        v.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                        HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

        # Création du texte soit pour la distance (course infinie), soit pour le temps (400m et 400m haie)
        TEXTE = ""
        ANTIALIAS = True
        COULEUR = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 22
        CENTRE_X = False
        CENTRE_Y = True
        ARRIERE_PLAN = constantes.WHITE
        ECART = 5
        SEUL = True
        LARGEUR = 0
        HAUTEUR = 0
        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0.6
        SCALE_Y = 0
        SCALE_WIDTH = 0.2
        SCALE_HEIGHT = 0.05
        COULEUR_ARRIERE = constantes.WHITE
        BORDURE = 0

        if modejeu == "400m":
            CoreGame.tempsobj = text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                                          ARRIERE_PLAN, ECART, SEUL,
                                          v.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                          HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

        # Création du bouton pause
        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0.9
        SCALE_Y = 0
        LARGEUR = 0
        HAUTEUR = 0
        SCALE_WIDTH = 0.1
        SCALE_HEIGHT = 0.05
        COULEUR = constantes.BLACK
        ANTIALIAS = True
        COULEUR_TEXTE = constantes.BLACK
        ARRIERE_PLAN_TEXTE = None
        FONT = "Arial"  # arial bold normalement
        TAILLE_FONT = 30
        CENTRE_X = True
        CENTRE_Y = True
        ARRIERE_PLAN = constantes.WHITE
        ECART = 0
        BORDURE = 3

        button.BPause("| |", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
                      ARRIERE_PLAN,
                      ECART, v.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                      HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

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

        self.piste = image.Image(REPERTOIRE, v.View.screen, POSITION_X,
                            POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        LARGEUR = 0
        HAUTEUR = -175
        POSITION_X = 0
        POSITION_Y = 175
        SCALE_X = 0
        SCALE_Y = 0.45
        SCALE_WIDTH = 1
        SCALE_HEIGHT = 0.55
        COULEUR = constantes.WHITE
        BORDURE = 0
        ALPHA = 255  # opque
        CONVERT_ALPHA = False

        self.surface_boutons = surface.Surface(ALPHA, CONVERT_ALPHA, v.View.screen, POSITION_X, POSITION_Y, SCALE_X,
                                               SCALE_Y, LARGEUR,
                                               HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                               BORDURE)

        CoreGame.surface_boutons = self.surface_boutons

        # Initialisation de la carte (IL FAUT TENIR COMPTE DE LA CARTE CHOISI !!)
        if carte == "Jeux Olympiques":
            CoreGame.mapscript = jo

        CoreGame.mapscript.init()

        POSITION_X = 0
        POSITION_Y = 65
        SCALE_X = 0.85
        SCALE_Y = 0.35

        CoreGame.characters_sprite.append(
            Character(constantes.CharactersFeatures["gros"], constantes.Animations["gros"], POSITION_X, POSITION_Y,
                      SCALE_X,
                      SCALE_Y))  # plus tard dans le développement du jeu, on devra  selectionner le sprite qui convient !

    def loop(cls, passed=0):  # update l'arrière plan + chaque personnage

        if not CoreGame.pause:
            char = CoreGame.characters_sprite[0]  # ATENTION: NE MARCHE QU'EN MODE 1 JOUEUR !!!
            # Calcul de la nouvelle distance parcouru
            charspeed = char.speed

            d1 = CoreGame.distance
            d2 = d1 + charspeed * (passed / 1000)
            delta_d = d2 - d1
            delta_pixel = int(d2 * 10) - int(d1 * 10)

            CoreGame.distance += delta_d
            CoreGame.time += passed
            new_distance = CoreGame.distance

            """Détermination de s'il faut dessiner la ligne d'arrivée ou pas"""
            # Calcul de la position x absolue du personnage
            char_absx = int(v.View.screen.abswidth * char.scalex + char.x)
            delta_pix_arrive = (400 - new_distance) * 10  # nombre de pixels avant d'arriver à la ligne d'arrivé (par rapport à la position du personnage)
            pos_x_ligne_arrive = char_absx - delta_pix_arrive

            if pos_x_ligne_arrive > -2:
                if not CoreGame.lignearriveobj:  # dessiner la ligne d'arrivé si elle n'existe pas encore
                    LARGEUR = 4
                    HAUTEUR = 175
                    POSITION_X = pos_x_ligne_arrive - 2
                    POSITION_Y = 0
                    SCALE_X = 0
                    SCALE_Y = 0.35
                    SCALE_WIDTH = 0
                    SCALE_HEIGHT = 0
                    COULEUR = constantes.WHITE
                    BORDURE = 0
                    ALPHA = 255  # opaque
                    CONVERT_ALPHA = False

                    CoreGame.lignearriveobj = surface.Surface(ALPHA, CONVERT_ALPHA, v.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

                else:  # sinon, on met juste à jour sa position
                    CoreGame.lignearriveobj.x = pos_x_ligne_arrive - 2

            # Mise à jour de l'affichage de la vitesse
            # Affichage de la vitesse du personnage en km/h
            CoreGame.vitesseobj.text = str(int(charspeed * 3.6)) + " km/h"

            # Mise à jour des boutons à appuyer
            key.Key.updatekeys(passed)

            # Affichage du temps en 400m et 400m haie
            if CoreGame.modejeu == "400m" or CoreGame.modejeu == "400m haie":
                temps_ms = CoreGame.time
                aff_ms = str(temps_ms % 1000)
                temps_s = int(temps_ms // 1000)
                aff_s = temps_s % 60
                temps_min = int(temps_s // 60)

                if aff_s < 10:
                    aff_s = "0" + str(aff_s)
                else:
                    aff_s = str(aff_s)

                CoreGame.tempsobj.text = str(temps_min) + ":" + aff_s + "." + aff_ms

            # On vérifie que l'on as pas atteint la distance nécessaire
            if CoreGame.modejeu == "400m" or CoreGame.modejeu == "400m haie":
                if new_distance >= 400:
                    CoreGame.finished = True
                    CoreGame.pause = True
                    eg.EndGame(CoreGame.modejeu, CoreGame.carte, new_distance, CoreGame.time, "end").end()

            # On vérifie qu'il as assez d'énergie pour continuer. Si son énergie est nulle, il tombe est c'est fini
            if char.energy <= 0:
                CoreGame.finished = True
                eg.EndGame(CoreGame.modejeu, CoreGame.carte, new_distance, CoreGame.time, "energy").end()

            # Apparition aléatoire de touches sur lesquels appuyer (qui dépend du mode de jeu)
            if new_distance == 0:
                new_distance = 0.1  # pas de division par 0 !

            if CoreGame.modejeu == "400m" or CoreGame.modejeu == "400m haie":
                key_chance = int(1000 / new_distance)  # la probabilité d'avoir une touche augmente avec la distance parcouru
            else:  # course infinie
                key_chance = int(new_distance**0.5 / new_distance / 1000)

            # TODO: Créé un crash en course infini:
            if random.randint(1, key_chance) == 1 and key.Key.canCreateKey():
                key.Key(CoreGame.surface_boutons, 10)  # timeout qui dépend de la difficulté

            for decors in CoreGame.mapscript.getDecors():
                for surfaceobj in decors:
                    surfaceobj.x += delta_pixel

            # Mis à jour de l'arrière plan de la carte
            CoreGame.mapscript.refresh()

            # Mis à jour du state, et calcul de la vitesse, de la hauteur du saut...
            for character in CoreGame.characters_sprite:
                state_sprite = character.__getattribute__(character.state + "sprite")
                characterinfos = character.characterinfos
                extra_y_offset = 0
                if character.running:
                    new_state = "run"
                    character.runsprite.adjustspeed(character.speed*6)
                elif character.jumping:
                    jump_compteur = character.jumpsprite.totalcompteur
                    if jump_compteur == 27:  # atterissage d'un saut
                        new_state = "run"
                        character.run()
                    else:
                        new_state = "jump"
                        extra_y_offset = (1 / 2) * jump_compteur ** 2 - 13 * jump_compteur  # hauteur du saut parabolique :p
                        extra_y_offset = extra_y_offset
                else:
                    new_state = "idle"  # fin et début de la course

                if character.state != new_state:  # si le personnage change d'état...
                    character.__getattribute__(character.state + "sprite").reset()  # on remet à 0 son animation

                character.changeState(new_state)

                # Chargement de la prochaine image du personnage
                character.__getattribute__(new_state + "sprite").next(
                    -int(characterinfos[new_state]["framesize"][0] / 2),
                    -int(characterinfos[new_state]["framesize"][1] / 2) + extra_y_offset)

            # Mis à jour de la taille et la couleur de la barre d'énergie
            CoreGame.barre_energie_in.scalew = char.energy / char.characterfeatures["initenergy"]
            if char.energy >= 70:
                CoreGame.barre_energie_in.color = constantes.GREEN
            elif char.energy >= 30:
                CoreGame.barre_energie_in.color = constantes.YELLOW
            else:
                CoreGame.barre_energie_in.color = constantes.RED

            """ TODO: Debug
            CoreGame.finished = True
            CoreGame.pause = True
            eg.EndGame(CoreGame.modejeu, CoreGame.carte, new_distance, CoreGame.time, "debug").end()"""

    def keypressed(cls, pygame, event):
        if event.key == pygame.K_SPACE:
            CoreGame.characters_sprite[0].jump()  # Ici, le joueur 1 saute
        else:
            key.Key.keypressed(event.dict["unicode"].capitalize())

    def getCharacterSprites(cls):
        return CoreGame.characters_sprite

    loop = classmethod(loop)
    keypressed = classmethod(keypressed)
    getCharacterSprites = classmethod(getCharacterSprites)
