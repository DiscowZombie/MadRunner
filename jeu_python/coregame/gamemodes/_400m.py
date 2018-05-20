from coregame import coregame as coregame

import functions
import userstatistics


class _400m:
    dist_to_travel = 400
    disp_function = None  # va être mis plus tard lors de l'initialisation
    score_text = "time"
    coursetype = "Q"

    def __init__(self):
        _400m.disp_function = functions.computetime

    def refresh(self):
        pass

    def computescore(self):  # le score dépend du temps
        return 100000000 / coregame.CoreGame.current_core.time  # Prendre en compte la difficulité?

    def isrecord(self, level, gm_score):
        return gm_score < userstatistics.UserStatistics.stats.best_gm_score[level]["400m"]

    def unreferance(self):
        pass

    @classmethod
    def computekeychance(cls):
        return int(1000 / coregame.CoreGame.current_core.distance)
