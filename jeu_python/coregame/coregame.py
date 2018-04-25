import functions
import uielement
from uielements import button as button
from uielements import image as image
from uielements import surface as surface
from uielements import rect as rect
from uielements import text as text
import statemanager

import coregame.spritesheet as sprit
import coregame.gameobjects.key as key
import coregame.difficulty as difficulty

import coregame.mapscripts.jeuxolympiques as jo
import coregame.mapscripts.foret as foret
import coregame.mapscripts.athenes as athenes

import coregame.gamemodes._400m as _400m
import coregame.gamemodes._400mhaie as _400mhaie
import coregame.gamemodes.courseinfinie as courseinfinie

import constantes
import view as v
import model
import userstatistics

import random

"""
Ne fonctionne pour pour 60 fps pour le moment
"""


class Character:
    characters = []

    def __init__(self, characterfeatures, characterinfos, posx, posy, scalex, scaley, initdist):
        for spritename in characterinfos:
            self.__setattr__(spritename + "sprite",
                             sprit.SpriteStripAnim(characterinfos[spritename]))
        self.characterinfos = characterinfos
        self.characterfeatures = characterfeatures
        self.x = posx
        self.y = posy
        self.scalex = scalex
        self.scaley = scaley
        self.absx = int(v.View.screen.abswidth * self.scalex + self.x)
        self.absy = int(v.View.screen.absheight * self.scaley + self.y)
        self.state = "run"
        self.running = True  # on va supposer pour l'instant que le gars cour tout de suite, mais plus tard, ce ne sera pas le cas (car on montrera un 3,2,1, go !)
        self.jumping = False  # le personnage est-il en train de sauter ?
        self.energy = characterfeatures["initenergy"]
        self.speed = characterfeatures["initspeed"]
        self.distance = initdist  # distance du personnage par rapport à la ligne de départ

        Character.characters.append(self)

    def run(self):
        self.running = True
        self.jumping = False

    def jump(self):
        if not self.jumping and self.energy > 10:
            self.energy -= 10
            self.speed -= 0.3  # Sauter reduit sa vitesse de 0.3 m/s (1.08 km/h)
            self.jumping = True
            self.running = False
            userstatistics.UserStatistics.stats.increment("nb_sauts", 1)

    def changeState(self, new_state):
        self.state = new_state

    def boost(self, attribut,
              amount):  # permet d'augmenter la valeur d'un attribut (ou de le diminuer si amount est négatif)
        if attribut == "energy":  # petite exception pour cette attribut qui ne peut excéder la quantité d'énergie initiale
            max_energy = self.characterfeatures["initenergy"]
            if self.energy + amount > max_energy:
                amount = max_energy - self.energy
        if self.__getattribute__(attribut) + amount < 0:  # pour empêcher d'avoir de valeurs négatives !
            amount = -self.__getattribute__(attribut)
        self.__setattr__(attribut, self.__getattribute__(attribut) + amount)

    def unreferance(self):
        for spritename in self.characterinfos:
            self.__getattribute__(spritename + "sprite").unreferance()
        Character.characters.remove(self)

    def getCharacters(cls):
        return Character.characters

    getCharacters = classmethod(getCharacters)


class CoreGame:
    current_core = None  # l'objet core (la partie en gros)

    def __init__(self, carte, modejeu, level):
        """
        :param carte - La carte sélectionnée. Valeurs possibles: Jeux Olympiques, Athènes, Forêt
        :param modejeu - Le mode de jeu sélectionné. Valeurs possibles: 400m, 400m haie, Course infinie
        :param level - Le niveau sélectionné. Valeurs possibles: Facile, Moyen, Difficile
        """

        functions.delete_menu_obj()
        for img in list(image.Image.getImages()):
            img.unreferance()

        statemanager.StateManager.setstate(statemanager.StateEnum.PLAYING)

        self.time = 0
        self.distance = 0
        self.score = 0
        self.gamemode_score = 0
        self.pause = False
        self.finished = False
        self.carte = carte
        self.modejeu = modejeu
        self.level = level
        self.lignearriveobj = None
        self.reason = None  # la raison de la fin du jeu. N'existe que lorsque self.end() est appelé
        self.error = None  # l'erreur si jamais la requête d'envoie du score échoue. N'existe que si la requête en fin de partie échoue

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

        self.barre_energie_out = surface.Surface(ALPHA, CONVERT_ALPHA, v.View.screen, POSITION_X, POSITION_Y,
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

        self.barre_energie_in = rect.Rect(self.barre_energie_out, POSITION_X, POSITION_Y, SCALE_X,
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

        self.vitesseobj = text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
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

        self.game_mode_disp = text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y,
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

        image.Image(REPERTOIRE, v.View.screen, POSITION_X,
                    POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                    BORDURE)

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

        CoreGame.current_core = self

        # Chargement du personnage
        POSITION_X = 0
        POSITION_Y = 65
        SCALE_X = 0.85
        SCALE_Y = 0.35
        INITDIST = 0

        self.personnage = functions.getrunner()  # le personnage avec lequel le joueur va jouer

        Character(constantes.CharactersFeatures[self.personnage], constantes.Animations[self.personnage], POSITION_X, POSITION_Y,
                  SCALE_X, SCALE_Y, INITDIST)  # plus tard dans le développement du jeu, il faudra  selectionner le sprite qui convient !

        # Initialisation de la carte et du mode de jeu
        if carte == "Jeux Olympiques":
            self.mapclass = jo.JeuxOlympiques
        elif carte == "Forêt":
            self.mapclass = foret.Foret
        elif carte == "Athènes":
            self.mapclass = athenes.Athenes

        if modejeu == "400m":
            self.gamemodeclass = _400m._400m
        elif modejeu == "400m haie":
            self.gamemodeclass = _400mhaie._400mHaie
        elif modejeu == "Course infinie":
            self.gamemodeclass = courseinfinie.CourseInfinie

        if level == "Facile":
            self.level_obj = difficulty.Facile()
        elif level == "Moyen":
            self.level_obj = difficulty.Moyen()
        elif level == "Difficile":
            self.level_obj = difficulty.Difficile()

        self.map_obj = self.mapclass()
        self.gamemode_obj = self.gamemodeclass()
        self.dist_to_travel = self.gamemodeclass.dist_to_travel
        self.disp_function = self.gamemodeclass.disp_function

    def loop(self, passed=0):  # update l'arrière plan + chaque personnage

        if not self.pause and not self.finished:
            char = Character.getCharacters()[0]  # ATENTION: NE MARCHE QU'EN MODE 1 JOUEUR !!!
            # Calcul de la nouvelle distance parcouru
            charspeed = char.speed

            d1 = self.distance
            d2 = d1 + charspeed * (passed / 1000)
            delta_pixel = int(d2 * 10) - int(d1 * 10)  # nombre de pixels décalés pour l'arrière plan

            self.distance = d2
            self.time += passed
            new_distance = self.distance
            char.distance = new_distance

            if self.dist_to_travel:
                """Détermination de s'il faut dessiner la ligne d'arrivée ou pas"""
                # Calcul de la position x absolue du personnage
                delta_pix_arrive = (
                                           400 - new_distance) * 25  # nb de pixels avant la ligne d'arrivé (par rapport à la position du personnage)
                pos_x_ligne_arrive = char.absx - delta_pix_arrive

                if pos_x_ligne_arrive > -2:
                    if not self.lignearriveobj:  # dessiner la ligne d'arrivé si elle n'existe pas encore
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

                        self.lignearriveobj = surface.Surface(ALPHA, CONVERT_ALPHA, v.View.screen, POSITION_X,
                                                              POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR,
                                                              SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

                    else:  # sinon, on met juste à jour sa position
                        self.lignearriveobj.x = pos_x_ligne_arrive - 2
                else:
                    if self.lignearriveobj:
                        self.lignearriveobj.unreferance()
                        self.lignearriveobj = None

                # Est-ce la fin du jeu ?
                if new_distance >= self.dist_to_travel:
                    self.end(True)
                    return

            # Mis à jour de la taille et la couleur de la barre d'énergie
            self.barre_energie_in.scalew = char.energy / char.characterfeatures["initenergy"]
            if char.energy >= 70:
                color = constantes.GREEN
            elif char.energy >= 30:
                color = constantes.YELLOW
            else:
                color = constantes.RED
            self.barre_energie_in.color = color

            # Vérifie qu'il y a assez d'énergie pour continuer. Si son énergie est nulle, il tombe est c'est fini
            if char.energy <= 0:
                self.end(False)
                return

            # Mise à jour de l'affichage de la vitesse
            # Affichage de la vitesse du personnage en km/h
            self.vitesseobj.text = str(int(charspeed * 3.6)) + " km/h"

            # Mise à jour des boutons à appuyer
            key.Key.updatekeys(passed)

            # Affichage du texte spécifique du mode de jeu (temps pour 400m et 400m haie, et distance pour course infinie)
            self.game_mode_disp.text = self.disp_function(False)

            # Apparition aléatoire de touches sur lesquels appuyer (qui dépend du mode de jeu)
            if new_distance == 0:
                new_distance = 0.01  # pas de division par 0 !

            key_chance = self.gamemodeclass.computekeychance()  # la probabilité d'avoir une touche qui s'affiche

            # TODO: Créé un crash en course infini:
            if random.randint(1, key_chance) == 1 and key.Key.canCreateKey():
                key.Key(self.surface_boutons, self.level_obj.keytimeout)  # timeout qui dépend de la difficulté

            for decors in self.map_obj.getDecors():
                for surfaceobj in decors:
                    surfaceobj.x += delta_pixel

            # Mis à jour du state + conséquences de son changement
            for character in Character.getCharacters():

                # Calcul de la position x des personnages autre que le joueur
                if character != char:
                    previous_dist = character.distance
                    new_dist = previous_dist + character.speed * (passed / 1000)
                    character.distance = new_dist
                    character.x = (new_distance - character.distance) * 25
                y = 0
                if character.running:
                    new_state = "run"
                    character.runsprite.adjustspeed(character.speed * 6)
                elif character.jumping:
                    t = character.jumpsprite.time/1000
                    z = (1 / 2) * 9.81 * t ** 2 - 8 * t  # physique
                    y = z * 25
                    if y > 0:
                        y = 0
                        new_state = "run"
                        character.run()
                    else:
                        new_state = "jump"
                else:
                    new_state = "idle"  # fin et début de la course

                if character.state != new_state:  # si le personnage change d'état...
                    character.__getattribute__(character.state + "sprite").reset()  # on remet à 0 son animation

                character.changeState(new_state)

                # Chargement de la prochaine image du personnage
                new_state_sprite = character.__getattribute__(new_state + "sprite")
                new_state_sprite.next(passed)
                new_state_sprite.updatepos(0, y)  # pas de x pour l'instant

        # Mis à jour du territoire du mode de jeu
        self.gamemode_obj.refresh()

        # Mis à jour de l'arrière plan de la carte
        self.map_obj.refresh()

        # Mis à jour de la grille (si elle existe)
        if self.level_obj.grille:
            self.level_obj.grille.updatecontent()

    def end(self, completed):
        self.finished = True

        for k in list(key.Key.getKeys()):
            k.unreferance()

        self.game_mode_disp.unreferance()
        self.gamemode_obj.unreferance()

        new_score_record = False
        new_gm_record = False
        if completed:
            num_score = self.gamemode_obj.computescore()
            self.score = "%.0f" % round(num_score, 0)  # Enlever les décimales du score
            self.gamemode_score, num_gm_score = self.disp_function(False), self.disp_function(True)
            self.sendscore()

            # Comparer au meilleur score (local)
            userstatistics.UserStatistics.stats.increment("score_total", num_score)
            if userstatistics.UserStatistics.stats.best_score[self.level][self.modejeu]:
                if num_score > userstatistics.UserStatistics.stats.best_score[self.level][self.modejeu]:
                    new_score_record = True
                    userstatistics.UserStatistics.stats.set("best_score", num_score, self.level, self.modejeu)
            else:
                userstatistics.UserStatistics.stats.set("best_score", num_score, self.level, self.modejeu)

            if userstatistics.UserStatistics.stats.best_gm_score[self.level][self.modejeu]:
                if self.gamemode_obj.isrecord(self.level, num_gm_score):
                    new_gm_record = True
                    userstatistics.UserStatistics.stats.set("best_gm_score", num_gm_score, self.level, self.modejeu)
            else:
                userstatistics.UserStatistics.stats.set("best_gm_score", num_gm_score, self.level, self.modejeu)
        else:
            self.score = "N/A"
            self.gamemode_score = "N/A"
            userstatistics.UserStatistics.stats.increment("nb_courses_echouees", 1)

        userstatistics.UserStatistics.stats.increment("nb_courses", 1)
        userstatistics.UserStatistics.stats.increment("total_dist", self.distance)
        userstatistics.UserStatistics.stats.save()

        # Création de l'écran de fin
        # Surface
        LARGEUR = 450
        HAUTEUR = 0
        POSITION_X = - LARGEUR // 2
        POSITION_Y = 0
        SCALE_X = 0.5
        SCALE_Y = 1
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.LIGHT_GRAY
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = False

        surf = surface.Surface(ALPHA, CONVERT_ALPHA, v.View.screen, POSITION_X, POSITION_Y,
                               SCALE_X, SCALE_Y, LARGEUR,
                               HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                               BORDURE)

        # Afficher le score
        TEXTE = "Score: " + self.score
        ANTIALIAS = True
        COULEUR = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 26
        CENTRE_X = False
        CENTRE_Y = True
        ARRIERE_PLAN = None
        ECART = 0
        SEUL = True
        LARGEUR = 200
        HAUTEUR = 25
        POSITION_X = 12
        POSITION_Y = 15
        SCALE_X = 0
        SCALE_Y = 0
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR_ARRIERE = None
        BORDURE = 0

        text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                  ECART, SEUL,
                  surf, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                  HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

        if new_score_record:
            TEXTE = "NOUVEAU RECORD !"
            ANTIALIAS = True
            COULEUR = constantes.RED
            FONT = "Arial"
            TAILLE_FONT = 20
            CENTRE_X = True
            CENTRE_Y = True
            ARRIERE_PLAN = None
            ECART = 0
            SEUL = True
            LARGEUR = 200
            HAUTEUR = 25
            POSITION_X = 225
            POSITION_Y = 15
            SCALE_X = 0
            SCALE_Y = 0
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = None
            BORDURE = 0

            text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                      ECART, SEUL,
                      surf, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                      HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

        # Afficher le score spécifique du mode de jeu (temps, distance...)
        TEXTE = self.gamemodeclass.score_text + ": " + self.gamemode_score
        ANTIALIAS = True
        COULEUR = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 26
        CENTRE_X = False
        CENTRE_Y = True
        ARRIERE_PLAN = None
        ECART = 0
        SEUL = True
        LARGEUR = 200
        HAUTEUR = 25
        POSITION_X = 12
        POSITION_Y = 50
        SCALE_X = 0
        SCALE_Y = 0
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR_ARRIERE = None
        BORDURE = 0

        text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                  ECART, SEUL,
                  surf, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                  HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

        if new_gm_record:
            TEXTE = "NOUVEAU RECORD !"
            ANTIALIAS = True
            COULEUR = constantes.RED
            FONT = "Arial"
            TAILLE_FONT = 20
            CENTRE_X = True
            CENTRE_Y = True
            ARRIERE_PLAN = None
            ECART = 0
            SEUL = True
            LARGEUR = 200
            HAUTEUR = 25
            POSITION_X = 225
            POSITION_Y = 50
            SCALE_X = 0
            SCALE_Y = 0
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = None
            BORDURE = 0

            text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                      ECART, SEUL,
                      surf, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                      HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

        if self.error:
            # Afficher l'erreur
            TEXTE = self.error
            ANTIALIAS = True
            COULEUR = constantes.RED
            FONT = "Arial"
            TAILLE_FONT = 16
            CENTRE_X = True
            CENTRE_Y = True
            ARRIERE_PLAN = None
            ECART = 0
            SEUL = True
            LARGEUR = 430
            HAUTEUR = 15
            POSITION_X = 10
            POSITION_Y = 315
            SCALE_X = 0
            SCALE_Y = 0
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = None
            BORDURE = 0

            text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                      ECART, SEUL,
                      surf, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                      HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

        def surf_tween_ended():
            # Image "End"
            # Charger l'image de fin

            new_runner = functions.getrunner()

            # Afficher des boutons
            POSITION_X = 10
            POSITION_Y = 335
            SCALE_X = 0
            SCALE_Y = 0
            LARGEUR = 430
            HAUTEUR = 35
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR = constantes.GRAY
            ANTIALIAS = True
            COULEUR_TEXTE = constantes.BLACK
            ARRIERE_PLAN_TEXTE = COULEUR
            FONT = "Arial"
            TAILLE_FONT = 24
            CENTRE_X = True
            CENTRE_Y = True
            ARRIERE_PLAN = COULEUR
            ECART = 0
            BORDURE = 0  # rempli

            bouton_menu = button.BRetourMenu("Retour au menu", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X,
                               CENTRE_Y,
                               ARRIERE_PLAN, ECART, surf, POSITION_X, POSITION_Y, SCALE_X,
                               SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)
            bouton_menu.visible = self.personnage == new_runner

            if self.personnage != new_runner:  # le personnage a-t-il évoluer ?

                TEXTE = "Félicitation ! Votre personnage s'est amélioré !"
                ANTIALIAS = True
                COULEUR = constantes.RED
                FONT = "Arial"
                TAILLE_FONT = 24
                CENTRE_X = True
                CENTRE_Y = True
                ARRIERE_PLAN = None
                ECART = 0
                SEUL = True
                LARGEUR = 400
                HAUTEUR = 25
                POSITION_X = 15
                POSITION_Y = 110
                SCALE_X = 0
                SCALE_Y = 0
                SCALE_WIDTH = 0
                SCALE_HEIGHT = 0
                COULEUR_ARRIERE = None
                BORDURE = 0

                text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                          ECART, SEUL,
                          surf, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                          HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

                # Surface sur laquelle le personnage est blité
                LARGEUR = 150
                HAUTEUR = 150
                POSITION_X = -70
                POSITION_Y = -35
                SCALE_X = 0.5
                SCALE_Y = 0.5
                SCALE_WIDTH = 0
                SCALE_HEIGHT = 0
                COULEUR = constantes.LIGHT_GRAY
                BORDURE = 0  # rempli
                ALPHA = 255  # opaque
                CONVERT_ALPHA = False

                surf_pers = surface.Surface(ALPHA, CONVERT_ALPHA, v.View.screen, POSITION_X, POSITION_Y,
                                       SCALE_X, SCALE_Y, LARGEUR,
                                       HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                       BORDURE)

                REPERTOIRE = constantes.CharactersFeatures[self.personnage]["image"]
                LARGEUR = 150
                HAUTEUR = 150
                POSITION_X = 0
                POSITION_Y = 0
                SCALE_X = 0
                SCALE_Y = 0
                SCALE_WIDTH = 0
                SCALE_HEIGHT = 0
                COULEUR = None
                BORDURE = 0

                self.old_pers = image.Image(REPERTOIRE, surf_pers, POSITION_X,
                                          POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                          BORDURE)

                self.old_pers.tween(
                    2,
                    [
                       {
                           "name": "width",
                           "value": 0
                        },
                        {
                            "name": "height",
                            "value": 0
                        },
                        {
                            "name": "x",
                            "value": 75
                        },
                        {
                            "name": "y",
                            "value": 75
                        },
                    ]

                )

                def surf_pers_end():
                    self.old_pers.unreferance()
                    self.old_pers = None

                    REPERTOIRE = constantes.CharactersFeatures[new_runner]["image"]
                    LARGEUR = 0
                    HAUTEUR = 0
                    POSITION_X = 75
                    POSITION_Y = 75
                    SCALE_X = 0
                    SCALE_Y = 0
                    SCALE_WIDTH = 0
                    SCALE_HEIGHT = 0
                    COULEUR = None
                    BORDURE = 0

                    new_pers = image.Image(REPERTOIRE, surf_pers, POSITION_X,
                                              POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                              BORDURE)

                    new_pers.tween(
                        2,
                        [
                            {
                                "name": "width",
                                "value": 150
                            },
                            {
                                "name": "height",
                                "value": 150
                            },
                            {
                                "name": "x",
                                "value": 0
                            },
                            {
                                "name": "y",
                                "value": 0
                            }
                        ],
                    )

                    def on_new_pers():
                        bouton_menu.visible = True

                    surf_pers.tween(
                        2,
                        [
                            {
                                "name": "alpha",
                                "value": 255
                            }
                        ],
                        on_new_pers
                    )

                surf_pers.tween(
                    2,
                    [
                        {
                            "name": "alpha",
                            "value": 0
                        }
                    ],
                    surf_pers_end
                )

        surf.tween(
            0.35,
            [
                {
                    "name": "scaley",
                    "value": 0.5
                },
                {
                    "name": "height",
                    "value": 380
                },
                {
                    "name": "y",
                    "value": -190
                }
            ],
            surf_tween_ended
        )

    def sendscore(self):
        # Clé associé avec la session
        """
        TODO [BUG]: Pour le moment, elle est sur None
        key = settings.StatsManager.session_key

        if key is None:
            return
        try:
            settings.CurlManager(constantes.WEBSITE_URI + "send_data.php?key=" + key + "&score=" +
                                 self.score + "&coursetype=" + self.gamemodeclass.coursetype)
        except pycurl.error:
            self.error = "An error happened when trying to send statistics to the web server !"
        """

    def unreferance(self):  # TODO: bien tout reset et bien retourner au menu (pas encore le cas)

        self.map_obj.unreferance()

        for character in list(Character.getCharacters()):
            character.unreferance()

        UIelements = uielement.UIelement.getUIelements()
        for classname in UIelements:
            for obj in list(UIelements[classname]):
                obj.unreferance()

        CoreGame.current_core = None

        statemanager.StateManager.setstate(statemanager.StateEnum.MAIN_MENU)
        model.Model.main_menu()

    def keypressed(cls, pygame, event):
        if not CoreGame.current_core.pause and not CoreGame.current_core.finished:
            if event.key == pygame.K_SPACE:
                Character.getCharacters()[0].jump()  # Ici, le joueur 1 saute
            else:
                key.Key.keypressed(event.dict["unicode"].capitalize())

    keypressed = classmethod(keypressed)
