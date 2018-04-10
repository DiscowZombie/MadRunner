import uielements.surface as surface
import uielements.image as image
import constantes
import view
import functions as f

bg_surfaces = []
bas_surfaces = []
surface_panneau = None


def siege(bg_surface, y):
    REPERTOIRE = f.resource_path("assets/img/decors/Jeux Olympiques/siege.png")
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


def colonne_siege(x):

    global bg_surfaces

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

    bg_surfaces.append(bg_surface)

    for y in range((bg_surface.absheight // 30) + 1):
        siege(bg_surface, y)


def panneau(bas_surface, x):

    global bas_surfaces

    REPERTOIRE = f.resource_path("assets/img/decors/Jeux Olympiques/bas_gradin.png")
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

    bas_surfaces.append(image.Image(REPERTOIRE, bas_surface, POSITION_X,
                                    POSITION_Y, SCALE_X, SCALE_Y, LARGEUR, HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                    BORDURE))


def init():
    global surface_panneau

    taille_ecran = (view.View.screen.abswidth, view.View.screen.absheight)

    # Mis en place du haut de l'arrière plan (gradins)
    # On va creer autant d'image du haut du gradin que nécessaire pour remplir la largeur et la hauteur de la surface

    for i in range((taille_ecran[0]//30) + 1):
        colonne_siege(i*30)

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

    surface_panneau = bas_surface

    # On va creer autant d'image du bas de gradin que nécessaire pour remplir la largeur de la surface

    for i in range((taille_ecran[0]//200) + 1):
        panneau(bas_surface, i*200)

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

    hors_piste_haut = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
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

    hors_piste_bas = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                BORDURE)


def refresh():
    taille_ecran = (view.View.screen.abswidth, view.View.screen.absheight)

    # HAUT DU GRADIN (SIèGES)
    max_x = 0
    min_x = taille_ecran[0]

    for surfaceimg in bg_surfaces:
        if surfaceimg.absx > taille_ecran[0]:  # on enlève dans un premier temps les sièges qui ne sont plus visibles
            bg_surfaces.remove(surfaceimg)
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
                for surfaceimg in bg_surfaces:
                    siege(surfaceimg, i)

    nbnouvcolonne = ((taille_ecran[0] - max_x)//30) + 1

    for i in range(nbnouvcolonne):  # ajout de colonnes de sièges s'il y a de la place à droite (redimension de l'écran)
        colonne_siege(max_x + i*30)

    if min_x >= 0:
        colonne_siege(min_x - 30)

    # BAS DU GRADIN (PANNEAUX)
    global surface_panneau
    global bas_surfaces

    max_x = 0
    min_x = taille_ecran[0]

    for surfaceimg in bas_surfaces:
        if surfaceimg.absx > taille_ecran[0]:  # on enlève dans un premier temps les panneaux qui ne sont plus visibles
            bas_surfaces.remove(surfaceimg)
            surfaceimg.unreferance()
        else:
            max_x = max(max_x,
                        surfaceimg.x + surfaceimg.abswidth)  # pour ajouter des colonnes de sièges si jamais l'écran est redimensionné (plus grand)
            min_x = min(min_x, surfaceimg.x)

    nbnouvcolonne = ((taille_ecran[0] - max_x)//200) + 1

    for i in range(nbnouvcolonne):  # ajout de colonnes de sièges s'il y a de la place
        panneau(surface_panneau, max_x + i*200)

    if min_x >= 0:
        panneau(surface_panneau, min_x - 200)


def getDecors():
    global bg_surfaces
    global bas_surfaces

    return [bg_surfaces, bas_surfaces]
