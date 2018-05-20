import json
import pycurl
import socket
import os
import certifi
from io import BytesIO
from threading import Thread

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


# Faire facilement des rêquetes web
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
        if DEBUG:  # Afficher pleins d'infos utiles pour debug
            cu.setopt(cu.VERBOSE, True)
        cu.setopt(pycurl.SSL_VERIFYPEER, 1)
        cu.setopt(pycurl.SSL_VERIFYHOST, 2)
        cu.setopt(pycurl.CAINFO, certifi.where())
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

        if not os.path.exists(
                FILE_PATH):  # si le jeu est lancé pour la première fois, ou si le fichier settings a été effacé
            file = open(FILE_PATH, "w")
            file.write(
                '{ "account_settings": { "username": null, "password": null }, "game_settings": { "limit_fps": 60 }, "debug": false }')
            file.close()

        readable_dict = JsonManager(FILE_PATH).readjson()

        if "language" not in readable_dict["game_settings"]:
            """ DETECTION DE LA LANGUE PAR DEFAUT DU SYSTEME """
            import locale
            import ctypes
            import translations
            kerneldll = ctypes.windll.kernel32
            language_code = locale.windows_locale[kerneldll.GetUserDefaultUILanguage()]
            language_id = language_code[:language_code.find("_")]
            if language_id not in translations.translations["play"]:  # si la langue du système n'est pas disponible, met le jeu en anglais
                language_id = "en"
            readable_dict["game_settings"]["language"] = language_id

            SettingsManager.current_settings = readable_dict
            SettingsManager.update_settings()
            return

        SettingsManager.current_settings = readable_dict

    """
    @classmethod est l'annotation permettant équivalente à 'update_settings = classmethod(update_settings)'
    Une méthode de class est comme une méthode static sauf qu'elle prends un object de class en paramètre et fonctionne donc avec la class
    """
    @classmethod
    def update_settings(
            cls):  # à appeler à chaque fois qu'on change un quelque chose dans les settings pour enregistrer les changements !
        f = open(FILE_PATH, "w")
        # Faire les convertions nécessaires entre python et le fichier json
        f.write(str(SettingsManager.current_settings).replace('False', 'false').replace('True', 'true').replace("'",
                                                                                                                '"').replace(
            'None', 'null'))
        f.close()
        SettingsManager()
