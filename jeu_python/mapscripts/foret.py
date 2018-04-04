import uielements.surface as surface
import uielements.image as image
import constantes
import view

bg_surfaces = []
ligne_vide = None  # l'objet surface qui compense le vide entre les arbres et la piste

def arbre(bg_surface, x):

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


def ligne_arbre(y):

    global bg_surfaces

    LARGEUR = 0
    HAUTEUR = 88
    POSITION_X = 0
    POSITION_Y = 88*y
    SCALE_X = 0
    SCALE_Y = 0.05
    SCALE_WIDTH = 1
    SCALE_HEIGHT = 0
    COULEUR = constantes.DARKGREEN
    BORDURE = 0  # rempli
    ALPHA = 255  # transparent
    CONVERT_ALPHA = False

    bg_surface = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                BORDURE)  # creation de la l'objet surface où on va mettre les arbres

    bg_surfaces.append(bg_surface)

    for i in range((bg_surface.abswidth//150) + 1):
        arbre(bg_surface, i*150 - 75*(len(bg_surfaces)%2))


def init():

    global ligne_vide

    taille_ecran = (view.View.screen.abswidth,view.View.screen.absheight)

    # Mis en place des arbres
    # On va creer autant d'image d'arbres que nécessaire pour remplir la largeur et la hauteur de la surface
    num_ligne = int(taille_ecran[1]*0.3)//88
    for y in range(int(taille_ecran[1]*0.3)//88):  # RAPPEL: *0.3 car la taille y de l'endoit où se trouve les arbres est 0.3 fois la taille y de l'écran
        ligne_arbre(y)

    # la ligne vide qui compense le vide entre les arbres et la piste
    LARGEUR = 0
    HAUTEUR = int(taille_ecran[1]*0.3) - num_ligne*88
    POSITION_X = 0
    POSITION_Y = num_ligne*88
    SCALE_X = 0
    SCALE_Y = 0.05
    SCALE_WIDTH = 1
    SCALE_HEIGHT = 0
    COULEUR = constantes.DARKGREEN
    BORDURE = 0  # rempli
    ALPHA = 255  # opaque
    CONVERT_ALPHA = False

    ligne_vide = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
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

    hors_piste_bas = surface.Surface(ALPHA, CONVERT_ALPHA, view.View.screen, POSITION_X, POSITION_Y, SCALE_X, SCALE_Y, LARGEUR,
                                HAUTEUR, SCALE_WIDTH, SCALE_HEIGHT, COULEUR,
                                BORDURE)


def refresh():
    taille_ecran = (view.View.screen.abswidth,view.View.screen.absheight)

    # RAFAÎCHISSMENT DES ARBRES
    max_y = 0

    for surfaceimg in bg_surfaces:
        if surfaceimg.absy + surfaceimg.absheight > taille_ecran[1]*0.35:  # on enlève dans un premier temps les lignes d'arbres qui ne sont plus visibles
            bg_surfaces.remove(surfaceimg)
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

            nbnouvarbre = (surfaceimg.abswidth - max_x)//150  # nombre de nouveaux arbres par ligne (à droite)

            for i in range(nbnouvarbre):  # ajout d'arbres s'il y a de la place à droite
                arbre(surfaceimg, max_x + i*150)

            if min_x >= 0:  # ajout d'arbres s'il y a de la place à gauche
                for i in range((min_x//150) + 1):
                    arbre(surfaceimg, min_x - 150)

    nbligne = len(bg_surfaces)
    nbnouvligne = int((taille_ecran[1]*0.3 - max_y)//88)

    for y in range(nbligne, nbligne + nbnouvligne):  # ajout de colonnes d'arbres s'il y a de la place
        ligne_arbre(y)

    global ligne_vide

    ligne_vide.y = len(bg_surfaces)*88
    ligne_vide.height = (int(taille_ecran[1]*0.3) - ligne_vide.y) + 1  # le +1 au cas ou ça arrondi en dessous (et donc ça créer un pixel d'écart blanc dégeulasse)


def getDecors():
    global bg_surfaces
    images = []

    for bg_surface in bg_surfaces:
        for image in bg_surface.children:
            images.append(image)

    return [images]
