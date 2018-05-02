import json
import pycurl
import socket
import os
from io import BytesIO
from threading import Thread
import settings

DEBUG = False

PATH = os.getenv('APPDATA') + "/MadRunner"
FILE_PATH = PATH + "/settings.json"


# Lire facilement les fichiers JSON \ Classe "privé"
class JsonManager:
    file = None

    def __init__(self, f):
        self.file = f

    def readjson(self):
        return json.load(open(self.file))


# Faire facilement des requetes web
class CurlManager(Thread):

    def __init__(self, uri, post, postfields, endfunction):
        Thread.__init__(self)

        self.uri = uri
        self.post = post
        self.postfields = postfields
        self.endfunction = endfunction
        self.hasinternet = True
        self.jsonresp = None

        self.start()

    def run(self):
        try:
            socket.create_connection(("www.google.com", 80))
        except:
            self.hasinternet = False
            self.endfunction(self)
            return  # pas de connection internet

        buffer = BytesIO()
        cu = pycurl.Curl()
        cu.setopt(cu.URL, self.uri)
        cu.setopt(cu.WRITEDATA, buffer)
        if self.post:
            cu.setopt(cu.POST, True)
            cu.setopt(cu.POSTFIELDS, self.postfields)
        if settings.DEBUG:  # Afficher pleins d'infos utiles pour debug
            cu.setopt(cu.VERBOSE, True)
        cu.perform()
        cu.close()
        self.jsonresp = buffer.getvalue().decode('iso-8859-1')
        self.endfunction(self)

    def readjson(self):
        if self.hasinternet:
            return self.jsonresp
        else:
            return False


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
"""
class StatsManager:

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
"""
