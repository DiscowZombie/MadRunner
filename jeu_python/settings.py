import json
import constantes as c
import pycurl
import os
from io import BytesIO

DEBUG = False

PATH = os.getenv('APPDATA') + "/MadRunner"
FILE_PATH = PATH + "/settings.json"

# TODO: On les sorts temporairement, après on passera plutot par un Singleton de la class StatsManager
# Cette variable correspond à une representation json du retour de create_session. Soit un id ["id"] et une clé de session ["key"]
response_json = None
# Cette variable contient les infos de course du joueur (meilleurs temps et temps dans chaque mode de jeu)
data = None


# Lire facilement les fichiers JSON \ Classe "privé"
class JsonManager:
    file = None

    def __init__(self, f):
        self.file = f

    def readjson(self):
        return json.load(open(self.file))


# Faire facilement des requetes web
class CurlManager:
    jsonresp = None

    def __init__(self, uri, post=False, postfields=None):
        buffer = BytesIO()
        cu = pycurl.Curl()
        cu.setopt(cu.URL, uri)
        cu.setopt(cu.WRITEDATA, buffer)
        if post:
            cu.setopt(cu.POST, True)
            cu.setopt(cu.POSTFIELDS, postfields)
        # TODO: Debug
        cu.setopt(cu.VERBOSE, True)
        cu.perform()
        cu.close()
        self.jsonresp = buffer.getvalue().decode('iso-8859-1')

    def readjson(self):
        return self.jsonresp


# Permet de récupérer les options du joueur (nombre de fps, etc...)
class SettingsManager:
    settings_file = None

    def __init__(self):
        if not os.path.exists(PATH):
            os.makedirs(PATH)

        if not os.path.exists(FILE_PATH):
            file = open(FILE_PATH, "w")
            file.write(
                '{ "account_settings": { "username": null, "password": null }, "game_settings": { "limit_fps": 60 }, "debug": false }')
            file.close()

        self.settings_file = JsonManager(FILE_PATH).readjson()

    def readjson(self):
        return self.settings_file


# Permet de récuprer les stats du joueur (nb de courses, etc...)
class StatsManager:
    username = None
    password = None

    def __init__(self):
        self.username = SettingsManager().readjson()["account_settings"]["username"]
        self.password = SettingsManager().readjson()["account_settings"]["password"]

        if DEBUG:
            print("[DEBUG] (settings.py > l.77) Username: " + ("NULL" if self.username is None else self.username))
            print("[DEBUG] (settings.py > l.78) Password: " + ("NULL" if self.password is None else self.password))

    def loadkey(self):
        if self.username is None or self.password is None:
            if DEBUG:
                print("[DEBUG] (settings.py > l.83) Using anonymous user.")
            return

        try:
            json_response = CurlManager(c.WEBSITE_URI + "create_session.php", True,
                                        "pseudo=" + self.username + "&password=" + self.password).readjson()
            if json_response is not None:
                if DEBUG:
                    print("[DEBUG] (settings.py > l.92) Succesfully loaded a new key for user " + self.username + ".")
                return json_response
        except pycurl.error:
            pass

        if DEBUG:
            print("[DEBUG] (settings.py > l.98) Can't load a key for user " + self.username + ".")

    @staticmethod
    def getusername():
        return SettingsManager().readjson()["account_settings"]["username"]
