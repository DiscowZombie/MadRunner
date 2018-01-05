from enum import Enum


class StateEnum(Enum):
    """
    Une énumration des états de jeu
    """
    MAIN_MENU = "",
    STATS_MENU = "",
    SETTINGS_MENU = "",
    PLAYING = ""


class StateManager:
    laststate = None  # None = Null (on peut utiliser if... is None)

    """
    Change l'état de jeu
    <p>
    :param state - L'état de jeu (un StateEnum ou None)
    """

    @staticmethod
    def setstate(state):
        StateManager.laststate = state

    @staticmethod
    def getstate():
        return StateManager.laststate