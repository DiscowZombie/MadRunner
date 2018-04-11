import constantes
import view as v
from uielements import surface as surface
from uielements import button as button
from uielements import text as text
from uielements import image as image
from coregame import coregame as coregame
import functions as f
import settings
import pycurl


class EndGame:
    # Empêcher de mettre en pause SSI on est déjà arriver ici
    score = 0
    reason = None
    carte = None
    modejeu = None
    error = None

    def __init__(self, modejeu, carte, distance, time, reason):
        if modejeu == "400m" or modejeu == "400 haie":
            """
            Exemples de score:
            
            Bon temps (0:50.000) -> 50000 => Score: 2k
            Mauvais temps (2:00:000) -> 200000 => Score: 500
            """
            self.score = (1 / time) * 100000000  # Prendre en compte la difficulité?
        else:
            self.score = distance * 100  # Prendre en compte la difficulité?
        self.carte = carte
        self.reason = reason
        self.modejeu = modejeu

        # Beau socre
        self.score = "%.0f" % round(self.score, 0)  # Enlever les décimales du score

        # Nettoyer l'écran
        coregame.CoreGame.getCharacterSprites().clear()
        for img in list(image.Image.getImages()):
            img.unreferance()
        f.delete_menu_obj()

        self.sendscore()

    def end(self):
        # Transition swag ?

        # Création de l'écran de fin

        # Surface
        LARGEUR = 500
        HAUTEUR = 420
        POSITION_X = 20
        POSITION_Y = 10
        SCALE_X = 0.05
        SCALE_Y = 0.03
        SCALE_WIDTH = 0.05  # TODO: A TRAVAILLER
        SCALE_HEIGHT = 0.03  # TODO: A TRAVAILLER
        COULEUR = constantes.YELLOW
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = False

        surf = surface.Surface(ALPHA, CONVERT_ALPHA, v.View.screen, POSITION_X, POSITION_Y,
                               SCALE_X, SCALE_Y, LARGEUR,
                               HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                               BORDURE)

        # Créé une image propre et l'afficher - Image "End"
        # ...

        # Afficher des boutons
        POSITION_X = 5
        POSITION_Y = 350
        SCALE_X = 0.05
        SCALE_Y = 0.03
        LARGEUR = 480
        HAUTEUR = 30
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0.03
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

        button.BRetourMenu("Retour au menu", ANTIALIAS, COULEUR_TEXTE, ARRIERE_PLAN_TEXTE, FONT, TAILLE_FONT, CENTRE_X,
                           CENTRE_Y,
                           ARRIERE_PLAN, ECART, surf, POSITION_X, POSITION_Y, SCALE_X,
                           SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

        # Afficher le score
        TEXTE = "Score: " + self.score
        ANTIALIAS = True
        COULEUR = constantes.BLACK
        FONT = "Arial"
        TAILLE_FONT = 30
        CENTRE_X = False
        CENTRE_Y = True
        ARRIERE_PLAN = constantes.WHITE
        ECART = 3
        SEUL = True
        LARGEUR = 0
        HAUTEUR = 0
        POSITION_X = 300
        POSITION_Y = 100
        SCALE_X = 0.2
        SCALE_Y = 0.2
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR_ARRIERE = constantes.WHITE
        BORDURE = 0

        text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                  ECART, SEUL,
                  surf, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                  HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

        if self.error is not None:
            # Afficher le score
            TEXTE = self.error
            ANTIALIAS = True
            COULEUR = constantes.BLACK
            FONT = "Arial"
            TAILLE_FONT = 14
            CENTRE_X = False
            CENTRE_Y = True
            ARRIERE_PLAN = constantes.WHITE
            ECART = 3
            SEUL = True
            LARGEUR = 0
            HAUTEUR = 0
            POSITION_X = 280
            POSITION_Y = 5
            SCALE_X = 0.22
            SCALE_Y = 0.22
            SCALE_WIDTH = 0
            SCALE_HEIGHT = 0
            COULEUR_ARRIERE = constantes.WHITE
            BORDURE = 0

            text.Text(TEXTE, ANTIALIAS, COULEUR, FONT, TAILLE_FONT, CENTRE_X, CENTRE_Y, ARRIERE_PLAN,
                      ECART, SEUL,
                      surf, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                      HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR_ARRIERE, BORDURE)

    def sendscore(self):
        # Clé associé avec la session
        key = settings.StatsManager.session_key

        if key is None:
            return

        # Coursetype
        coursetype = None
        if self.modejeu == "400m":
            coursetype = "Q"
        elif self.modejeu == "400 haie":
            coursetype = "QH"
        else:
            coursetype = "I"

        try:
            settings.BDDManager(
                constantes.WEBSITE_URI + "send_data.php?key=" + key + "&score=" + self.score + "&coursetype=" + coursetype)
        except pycurl.error:
            self.error = "A error as append when trying to send statistics to the web server!"
