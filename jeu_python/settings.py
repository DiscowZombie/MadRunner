import json
import constantes as c
import pycurl
import functions as f
from io import BytesIO


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
        self.settings_file = JsonManager(f.resource_path(c.CONFIG_PATH + "settings.json")).readjson()

    def readjson(self):
        return self.settings_file


# Permet de récuprer les stats du joueur (nb de courses, etc...)
class StatsManager:
    username = None
    password = None
    session_key = None

    def __init__(self):
        self.username = SettingsManager().readjson()["account_settings"]["username"]
        self.password = SettingsManager().readjson()["account_settings"]["password"]
        # TODO: Debug
        print("[DEBUG] (settings.py > l.62) Username: " + ("NULL" if self.username is None else self.username))
        print("[DEBUG] (settings.py > l.63) Password: " + ("NULL" if self.password is None else self.password))

    def loadkey(self):
        if self.username is None or self.password is None:
            print("[DEBUG] (settings.py > l.67) Using anonymous user.")
            return

        try:
            response = CurlManager(c.WEBSITE_URI + "create_session.php", True,
                                   "pseudo=" + self.username + "&password=" + self.password).readjson()
            if response is not None:
                self.session_key = response
                print("[DEBUG] (settings.py > l.75) Succesfully loaded a new key for user " + self.username + ".")
                return
        except pycurl.error:
            pass

        print("[DEBUG] (settings.py > l.80) Can't load a key for user " + self.username + ".")
