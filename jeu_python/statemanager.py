from enum import Enum


class StateEnum(Enum):
    """
    Une énumration des états de jeu
    """
    INITIALISATION = "init"
    INTRO = "intro"
    MAIN_MENU = "main_menu"
    PLAYERNUM = "num_player"
    MAP_AND_DIFF_SINGLE = "map_diff_single"
    MAP_AND_DIFF_MULTI = "map_diff_multi"
    MULTIPLAYER_MENU = "multiplayer_menu"
    MULTI_SERVERS_MENU = "multi_servers_menu"
    STATS_MENU = "stats_menu"
    BEST_SCORE = "best_score"
    AUTRE_STATS = "autre_stats"
    SETTINGS_MENU = "settings_menu"
    LANGUAGE_MENU = "language_menu"
    CONNEXION_MENU = "connexion_menu"
    UPDATE_MENU = "update_menu"
    PLAYING = "playing"


class StateManager:
    laststate = StateEnum.INITIALISATION
    statetime = 0

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
