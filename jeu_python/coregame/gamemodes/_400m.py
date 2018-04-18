from coregame import coregame as coregame
import functions


class _400m:

    dist_to_travel = 400
    disp_function = None  # va être mis plus tard lors de l'initialisation
    coursetype = "Q"

    def __init__(self):
        _400m.disp_function = functions.computetime

    def refresh(self):
        pass

    def computescore(self):  # le score dépend du temps
        return 100000000 / coregame.CoreGame.current_core.time  # Prendre en compte la difficulité?

    def unreferance(self):
        pass
