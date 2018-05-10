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

    current_settings = None  # les settings actuels (sous forme de dictionnaire)

    def __init__(self):
        if not os.path.exists(PATH):
            os.makedirs(PATH)

        if not os.path.exists(FILE_PATH):  # si le jeu est lancé pour la première fois, ou si le fichier settings a été effacé
            file = open(FILE_PATH, "w")
            file.write(
                '{ "account_settings": { "username": null, "password": null }, "game_settings": { "limit_fps": 60 }, "debug": false }')
            file.close()

        readable_dict = JsonManager(FILE_PATH).readjson()

        if not "language" in readable_dict["game_settings"]:
            """ DETECTION DE LA LANGUE PAR DEFAUT DU SYSTEME """
            import locale
            import ctypes
            import translations
            kerneldll = ctypes.windll.kernel32
            language_code = locale.windows_locale[kerneldll.GetUserDefaultUILanguage()]
            language_id = language_code[:language_code.find("_")]
            if not language_id in translations.translations["play"]:  # si la langue du système n'est pas disponible, met le jeu en anglais
                language_id = "en"

            readable_dict["game_settings"]["language"] = language_id

            file = open(FILE_PATH, "w")
            file.write(str(readable_dict).replace('False', 'false').replace('True', 'true').replace("'", '"').replace('None', 'null'))
            file.close()

        SettingsManager.current_settings = readable_dict

    def update_settings(cls):  # à appeler à chaque fois qu'on change un paramètre !
        SettingsManager()

    update_settings = classmethod(update_settings)


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
