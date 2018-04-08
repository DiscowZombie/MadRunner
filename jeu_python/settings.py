import json
import constantes as c
import pycurl
from io import BytesIO


class JsonManager:

    def __init__(self, f):
        self.file = f

    def readjson(self):
        return json.load(open(self.file))


class BDDManager:
    body = None

    """
    GET Request only
    """

    def __init__(self, website_url, ispost=False, posts=None):
        buffer = BytesIO()
        cu = pycurl.Curl()
        cu.setopt(cu.URL, website_url)
        if ispost:
            cu.setopt(cu.POSTFIELDS, posts)
        cu.setopt(cu.WRITEDATA, buffer)
        cu.perform()
        cu.close()
        self.body = buffer.getvalue()

    def readbdd(self):
        jsonbody = json.loads(self.body.decode('iso-8859-1'))
        return jsonbody


class Settings:

    def __init__(self):
        pass

    def get_conf_setting(self, array, setting_path):
        return JsonManager(c.CONFIG_PATH + "settings.json").readjson()[array][setting_path]

    """
    Read JSON - GET Request only"""

    def get_bdd_settings(self, url, setting_path):
        return BDDManager(url).readbdd()[setting_path]


class StatsManager:
    username = None
    password = None

    session_key = None

    def __init__(self):
        self.username = Settings().get_conf_setting("account_settings", "username")
        self.password = Settings().get_conf_setting("account_settings", "password")

    def loadKey(self):
        if self.username is None or self.password is None:
            return

        try:
            # TODO: A RETRAVAILLER, NE SEMBLE PAS FONCTIONNER
            resp = BDDManager(c.WEBSITE_URI + "create_session.php", True, '{ "pseudo": ' + self.username + ', "password": ' + self.password + ' }').readbdd()
            if resp is not None:
                self.session_key = resp
        except pycurl.error:
            pass

        return self.session_key
