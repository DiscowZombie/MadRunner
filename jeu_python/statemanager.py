from enum import Enum


class StateEnum(Enum):
    """
    Une énumration des états de jeu
    """
    INITIALISATION = "init"
    INTRO = "intro"
    MAIN_MENU = "main_menu"
    PLAYERNUM = "num_player"
    MAP_AND_DIFF = "map_diff"
    STATS_MENU = "stats_menu"
    BEST_SCORE = "best_score"
    AUTRE_STATS = "autre_stats"
    SETTINGS_MENU = "settings_menu"
    PLAYING = "playing"


class StateManager:
    laststate = StateEnum.INITIALISATION
    statetime = 0
    referancetimer = 0

    """
    :param state - L'état de jeu (un StateEnum ou None)
    """

    def setstate(cls, newstate):
        StateManager.laststate = newstate
        StateManager.statetime = 0

    def getstate(cls):
        return StateManager.laststate

    def setstatetime(cls, passed):
        StateManager.statetime += passed

    def getstatetime(cls):
        return StateManager.statetime

    setstate = classmethod(setstate)
    getstate = classmethod(getstate)
    setstatetime = classmethod(setstatetime)
    getstatetime = classmethod(getstatetime)
