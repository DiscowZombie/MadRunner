import settings
import functions


class GameSettings:

    fps = -1

    def setfps(self):
        self.fps = settings.SettingsManager().readjson()["game_settings"]["limit_fps"] if \
            functions.isvalidint(settings.SettingsManager().readjson()["game_settings"]["limit_fps"]) else \
            60
        return self.fps
