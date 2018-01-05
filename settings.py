import json
import constantes as c


class JsonManager:

    def __init__(self, f):
        self.file = f

    def readjson(self):
        return json.load(open(self.file))


class Settings:

    @staticmethod
    def getsetting(setting_path):
        return JsonManager(c.CONFIG_PATH + "settings.json").readjson()[setting_path]
