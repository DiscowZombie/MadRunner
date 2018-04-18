import uielements.surface as surface
import uielements.image as image
import constantes
import view


class JeuxOlympiques:

    def __init__(self):

        self.bg_surfaces = []
        self.bas_surfaces = []

        taille_ecran = (view.View.screen.abswidth, view.View.screen.absheight)

        # Mis en place du haut de l'arrière plan (gradins)
        # On va creer autant d'image du haut du gradin que nécessaire pour remplir la largeur et la hauteur de la surface

        for i in range((taille_ecran[0]//30) + 1):
            self.colonne_siege(i*30)

        # Mis en place du bas du gradin
        LARGEUR = 0
        HAUTEUR = 0
        POSITION_X = 0
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0.2
        SCALE_WIDTH = 1
        SCALE_HEIGHT = 0.1
        COULEUR = constantes.BLUE
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = False

        bas_surface = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                                      LARGEUR,
                                      HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                      BORDURE)  # creation de la l'objet surface où on va mettre les images du bas du gradin

        self.surface_panneau = bas_surface

        # On va creer autant d'image du bas de gradin que nécessaire pour remplir la largeur de la surface

        for i in range((taille_ecran[0]//200) + 1):
            self.panneau(i*200)

        # Mis en place du hors piste (avec une surface :p)
        # haut
        LARGEUR = 0
        HAUTEUR = 0
        POSITION_X = 0
        POSITION_Y = 0  # ne pas oublier que la piste a une hauteur de 175 pixels ! (ne dépend pas du scale, et donc de la taille de l'écran !)
        SCALE_X = 0
        SCALE_Y = 0.3
        SCALE_WIDTH = 1
        SCALE_HEIGHT = 0.05
        COULEUR = constantes.GREEN
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = False

        surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                    HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                    BORDURE)

        # bas
        LARGEUR = 0
        HAUTEUR = 0
        POSITION_X = 0
        POSITION_Y = 175
        SCALE_X = 0
        SCALE_Y = 0.35
        SCALE_WIDTH = 1
        SCALE_HEIGHT = 0.1
        COULEUR = constantes.GREEN
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = False

        surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                    HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                    BORDURE)

    def refresh(self):

        taille_ecran = (view.View.screen.abswidth, view.View.screen.absheight)

        # HAUT DU GRADIN (SIèGES)
        max_x = 0
        min_x = taille_ecran[0]

        for surfaceimg in self.bg_surfaces:
            if surfaceimg.absx > taille_ecran[0]:  # on enlève dans un premier temps les sièges qui ne sont plus visibles
                self.bg_surfaces.remove(surfaceimg)
                surfaceimg.unreferance()
            else:
                max_x = max(max_x,
                            surfaceimg.x + surfaceimg.abswidth)  # pour ajouter des colonnes de sièges si jamais l'écran est redimensionné (plus grand)
                min_x = min(min_x, surfaceimg.x)
                max_y = 0  # va servir a ajouter des sièges si jamais il en manque
                for image in surfaceimg.children:
                    if image.y > surfaceimg.absheight:
                        image.unreferance()
                    else:
                        max_y = max(max_y, image.y + image.absheight)  # pour ajouter des lignes de sièges

                nbsiege = len(surfaceimg.children)  # nombre de sièges de la colonne
                nbnouvsiege = ((surfaceimg.absheight - max_y) // 30) + 1  # nombre de nouveau siege par colonne

                for i in range(nbsiege, nbsiege + nbnouvsiege):  # ajout de colonnes de sièges s'il y a de la place
                    for surfaceimg in self.bg_surfaces:
                        self.siege(surfaceimg, i)

        nbnouvcolonne = ((taille_ecran[0] - max_x)//30) + 1

        for i in range(nbnouvcolonne):  # ajout de colonnes de sièges s'il y a de la place à droite (redimension de l'écran)
            self.colonne_siege(max_x + i*30)

        if min_x >= 0:
            self.colonne_siege(min_x - 30)

        # BAS DU GRADIN (PANNEAUX)
        max_x = 0
        min_x = taille_ecran[0]

        for surfaceimg in self.bas_surfaces:
            if surfaceimg.absx > taille_ecran[0]:  # on enlève dans un premier temps les panneaux qui ne sont plus visibles
                self.bas_surfaces.remove(surfaceimg)
                surfaceimg.unreferance()
            else:
                max_x = max(max_x,
                            surfaceimg.x + surfaceimg.abswidth)  # pour ajouter des colonnes de sièges si jamais l'écran est redimensionné (plus grand)
                min_x = min(min_x, surfaceimg.x)

        nbnouvcolonne = ((taille_ecran[0] - max_x)//200) + 1

        for i in range(nbnouvcolonne):  # ajout de colonnes de sièges s'il y a de la place
            self.panneau(max_x + i*200)

        if min_x >= 0:
            self.panneau(min_x - 200)

    def unreferance(self):
        for surf in self.bg_surfaces:
            surf.unreferance()
        for surf in self.bas_surfaces:
            surf.unreferance()

    def getDecors(self):
        return [self.bg_surfaces, self.bas_surfaces]

    def siege(self, bg_surface, y):
        REPERTOIRE = "assets/img/decors/Jeux Olympiques/siege.png"
        LARGEUR = 30
        HAUTEUR = 30
        POSITION_X = 0
        POSITION_Y = y * 30
        SCALE_X = 0
        SCALE_Y = 0
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0
        COULEUR = constantes.GRAY
        BORDURE = 0

        image.Image(REPERTOIRE, bg_surface, POSITION_X,
                    POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR, BORDURE)

    def colonne_siege(self, x):
        LARGEUR = 30
        HAUTEUR = 0
        POSITION_X = x
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0.05
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 0.15
        COULEUR = constantes.GRAY
        BORDURE = 0  # rempli
        ALPHA = 255  # opaque
        CONVERT_ALPHA = False

        bg_surface = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y,
                                     LARGEUR,
                                     HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                     BORDURE)  # creation de la l'objet surface où on va mettre le haut des gradins (les sièges)

        self.bg_surfaces.append(bg_surface)

        for y in range((bg_surface.absheight // 30) + 1):
            self.siege(bg_surface, y)

    def panneau(self, x):
        REPERTOIRE = "assets/img/decors/Jeux Olympiques/bas_gradin.png"
        LARGEUR = 200
        HAUTEUR = 0
        POSITION_X = x
        POSITION_Y = 0
        SCALE_X = 0
        SCALE_Y = 0
        SCALE_WIDTH = 0
        SCALE_HEIGHT = 1
        COULEUR = constantes.WHITE
        BORDURE = 0

        self.bas_surfaces.append(image.Image(REPERTOIRE, self.surface_panneau, POSITION_X,
                                        POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                        BORDURE))
