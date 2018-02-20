import settings
import functions


class GameSettings:

    fps = -1

    def setfps(self):
        self.fps = settings.Settings().get_conf_setting("limit_fps") if \
            functions.isvalidint(settings.Settings().get_conf_setting("limit_fps")) else \
            60
        return self.fps
