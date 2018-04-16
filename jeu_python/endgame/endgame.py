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

    def __init__(self, modejeu, script_modejeu, carte, script_carte, distance, time, reason):

        coregame.CoreGame.finished = True

        self.score = script_modejeu.computescore()
        self.carte = carte
        self.reason = reason
        self.modejeu = modejeu

        # Beau score
        self.score = "%.0f" % round(self.score, 0)  # Enlever les décimales du score

        # TODO: Nettoyer l'écran

        # Envoyé le score au serveur web
        self.sendscore()

    def end(self):
        # Transition swag ?

        # Création de l'écran de fin

        # Surface
        LARGEUR = 400
        HAUTEUR = 380
        POSITION_X = - LARGEUR//2
        POSITION_Y = - HAUTEUR//2
        SCALE_X = 0.5
        SCALE_Y = 0.5
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

        # Image "End"
        # Charger l'image de fin

        # Afficher des boutons
        POSITION_X = 10
        POSITION_Y = 335
        SCALE_X = 0
        SCALE_Y = 0
        LARGEUR = 380
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
