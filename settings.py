import json
import constantes as c

class JsonManager:

    def __init__(self, f):
        self.file = f

    def readJSON(self):
        return json.load(open(self.file))

class Settings:

    def getSetting(self, setting_path):
        return JsonManager(c.CONFIG_PATH+"settings.json").readJSON()[setting_path]
