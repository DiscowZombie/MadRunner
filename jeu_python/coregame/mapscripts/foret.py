import uielements.surface as surface
import uielements.image as image
import constantes
import view


class Foret:

    def __init__(self):

        self.bg_surfaces = []

        taille_ecran = (view.View.screen.abswidth, view.View.screen.absheight)

        # Mis en place des arbres
        # On va creer autant d'image d'arbres que nécessaire pour remplir la largeur et la hauteur de la surface
        num_ligne = int(taille_ecran[1] * 0.3) // 88
        for y in range(int(taille_ecran[
                               1] * 0.3) // 88):  # RAPPEL: *0.3 car la taille y de l'endoit où se trouve les arbres est 0.3 fois la taille y de l'écran
            self.ligne_arbre(y)

        # la ligne vide qui compense le vide entre les arbres et la piste
        LARGEUR = 0
        HAUTEUR = int(taille_ecran[1] * 0.3) - num_ligne * 88
        POSITION_X = 0
        POSITION_Y = num_ligne * 88
        SCALE_X = 0
        SCALE_Y = 0.05
        SCALE_WIDTH = 1
        SCALE_HEIGHT = 0
        COULEUR = constantes.DARKGREEN
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = False

        self.ligne_vide = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X,
                                          SCALE_Y, LARGEUR,
                                          HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                          BORDURE)

        # hors piste bas
        LARGEUR = 0
        HAUTEUR = 0
        POSITION_X = 0
        POSITION_Y = 175
        SCALE_X = 0
        SCALE_Y = 0.35
        SCALE_WIDTH = 1
        SCALE_HEIGHT = 0.1
        COULEUR = constantes.DARKGREEN
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = False

        surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                        HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                        BORDURE)

    def refresh(self):

        taille_ecran = (view.View.screen.abswidth, view.View.screen.absheight)

        # RAFAÎCHISSMENT DES ARBRES
        max_y = 0

        for surfaceimg in self.bg_surfaces:
            if surfaceimg.absy + surfaceimg.absheight > taille_ecran[
                1] * 0.35:  # on enlève dans un premier temps les lignes d'arbres qui ne sont plus visibles
                self.bg_surfaces.remove(surfaceimg)
                surfaceimg.unreferance()
            else:
                max_y = max(max_y, surfaceimg.y + surfaceimg.absheight)
                max_x = 0
                min_x = taille_ecran[0]
                for image in surfaceimg.children:  # enlève les arbres (dans les lignes d'arbres) qui ne sont plus visibles
                    if image.x > surfaceimg.abswidth:
                        image.unreferance()
                    else:
                        max_x = max(max_x, image.x + image.abswidth)
                        min_x = min(min_x, image.x)

                nbnouvarbre = (surfaceimg.abswidth - max_x) // 150  # nombre de nouveaux arbres par ligne (à droite)

                for i in range(nbnouvarbre):  # ajout d'arbres s'il y a de la place à droite
                    self.arbre(surfaceimg, max_x + i * 150)

                if min_x >= 0:  # ajout d'arbres s'il y a de la place à gauche
                    for i in range((min_x // 150) + 1):
                        self.arbre(surfaceimg, min_x - 150)

        nbligne = len(self.bg_surfaces)
        nbnouvligne = int((taille_ecran[1] * 0.3 - max_y) // 88)

        for y in range(nbligne, nbligne + nbnouvligne):  # ajout de colonnes d'arbres s'il y a de la place
            self.ligne_arbre(y)

        self.ligne_vide.y = len(self.bg_surfaces) * 88
        self.ligne_vide.height = (int(taille_ecran[
                                          1] * 0.3) - self.ligne_vide.y) + 1  # le +1 au cas ou ça arrondi en dessous (et donc ça créer un pixel d'écart blanc dégeulasse)

    def unreferance(self):
        for surf in self.bg_surfaces:
            surf.unreferance()

    def getDecors(self):
        images = []

        for bg_surface in self.bg_surfaces:
            for image in bg_surface.children:
                images.append(image)

        return [images]

    def arbre(self, bg_surface, x):

        REPERTOIRE = "assets/img/decors/Forêt/background.png"
        LARGEUR = 150
        HAUTEUR = 88
        POSITION_X = x
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = None
        BORDURE = 0

        image.Image(REPERTOIRE, bg_surface, POSITION_X,
                    POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

    def ligne_arbre(self, y):

        LARGEUR = 0
        HAUTEUR = 88
        POSITION_X = 0
        POSITION_Y = 88 * y
        SCALE_X = 0
        SCALE_Y = 0.05
        SCALE_WIDTH = 1
        SCALE_HEIGHT = 0
        COULEUR = constantes.DARKGREEN
        BORDURE = 0  # rempli
        ALPHA = 255  # transparent
        CONVERT_ALPHA = False

        bg_surface = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                                     LARGEUR,
                                     HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                     BORDURE)  # creation de la l'objet surface où on va mettre les arbres

        self.bg_surfaces.append(bg_surface)

        for i in range((bg_surface.abswidth // 150) + 1):
            self.arbre(bg_surface, i * 150 - 75 * (len(self.bg_surfaces) % 2))
