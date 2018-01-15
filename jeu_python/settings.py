import json
import constantes as c


class JsonManager:

    def __init__(self, f):
        self.file = f

    def readjson(self):
        return json.load(open(self.file))


class BDDManager:

    def __init__(self):
        print()

    def readbdd(self):
        # Make Web Request and Read returned json
        return None


class Settings:

    def __init__(self):
        print()

    def get_conf_setting(self, setting_path):
        return JsonManager(c.CONFIG_PATH + "settings.json").readjson()[setting_path]

    def get_bdd_settings(self, setting_path):
        return None
