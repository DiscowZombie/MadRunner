from coregame import coregame as coregame
import functions


def init():
    coregame.CoreGame.dist_to_travel = 400
    coregame.CoreGame.disp_function = functions.computetime


def refresh():
    pass


def computescore():  # le score dépend du temps
    return 100000000 / coregame.CoreGame.time  # Prendre en compte la difficulité?
