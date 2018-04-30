import constantes as c
import settings
import pycurl
import json


class OnlineConnector:
    # Never None, sauf si on y accede "directement" sans instance de class

    current_connection = None

    """
    Préparer l'ouverture d'une connexion pour l'utilisateur
    Si username et password sont None, on va prendre ceux de la config
    Si save vaut True, on sauvegarde username et password s'ils sont corrects (= qu'il n'y a pas eu d'erreur)
    """

    def __init__(self, username=None, password=None, save=False):
        self.connected = False
        self.internet = True
        self.responsejson = None  # Contient la réponse du serveur web (contient ["id"] et ["key"]. On admet que la connexion a été opéré sans soucis si elle est "not None"
        self.data = None  # Les stats du joueur
        if username is None:
            username = settings.SettingsManager().readjson()["account_settings"]["username"]
        if password is None:
            password = settings.SettingsManager().readjson()["account_settings"]["password"]

        self.username = username
        self.password = password
        self.save = save

        if OnlineConnector.current_connection:
            OnlineConnector.current_connection = None
        OnlineConnector.current_connection = self

    """
    Retourne "True" si la connexion s'est oppéré sans soucis, sinon une exception (pycurl.error ou Exception)
    Se connecter genère une clé unique de session
    """

    def connect(self):
        # S'ils sont encore nulles, on s'arrete ici
        if self.username is None or self.password is None:
            if settings.DEBUG:
                print("[DEBUG] (onlineconnector > l.33) Username or password is still None, aborted.")
            return

        try:
            json_response = settings.CurlManager(c.WEBSITE_URI + "create_session.php", True,
                                                 "pseudo=" + self.username + "&password=" + self.password).readjson()
            if json_response is not None and json_response is not False and json_response != "":
                self.responsejson = json_response
                if self.save:  # On sauvegarde les identifiants en config
                    json_rep = settings.SettingsManager().readjson()
                    json_rep["account_settings"][
                        "username"] = "null" if self.username is None else self.username
                    json_rep["account_settings"][
                        "password"] = "null" if self.password is None else self.password

                    f = open(settings.FILE_PATH, "w")
                    f.write(str(json_rep).replace('False', 'false').replace('True', 'true').replace("'", '"'))
                    f.close()
                self.connected = True
            elif json_response is False:
                self.internet = False
            else:
                if settings.DEBUG:
                    print("[DEBUG] (onlineconnector > l.63) An error as append (bad username or password ?)")
                raise BaseException("Json response seems null: Bad username or password ?")
        except pycurl.error as e:
            if settings.DEBUG:
                print("[DEBUG] (onlineconnector > l.67) An error as append !")
            raise e

    """
    Retourne True si les stats se sont bien chargés, sinon une Exception()
    """

    def loadstatistiques(self):
        if not self.connected or self.responsejson is None:
            if settings.DEBUG:
                print("[DEBUG] (onlineconnector > l.78) Can't load statistics of anonymous !")
            raise BaseException("Can't load statistics of anonymous")

        user_id = json.loads(self.responsejson)['id']

        if user_id is None or user_id == 0:
            if settings.DEBUG:
                print("[DEBUG] (onlineconnector > l.85) user_id seems null or zero !")
            raise BaseException("user_id seems null or zero")

        data = settings.CurlManager(c.WEBSITE_URI + "statistiques.php?id=" + user_id).readjson()

        if data is None or data == "":
            if settings.DEBUG:
                print("[DEBUG] (onlineconnector > l.92) Server web reponse is null")
            raise BaseException("Server web response is null")

        self.data = data

    """
    Si clearidentifiants vaut True, on met à null ses identifiants en config
    Disconnect va forcement détuire l'objet
    """

    def disconnect(self, clearidentifiants=False):
        self.connected = False
        self.current_connection = None

        if clearidentifiants:
            json_rep = settings.SettingsManager().readjson()
            json_rep["account_settings"][
                "username"] = "null"
            json_rep["account_settings"][
                "password"] = "null"

            f = open(settings.FILE_PATH, "w")
            f.write(str(json_rep).replace('False', 'false').replace('True', 'true').replace("'", '"').replace('"null"',
                                                                                                              'null'))
            f.close()
