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

    def __init__(self, website_url):
        buffer = BytesIO()
        cu = pycurl.Curl()
        cu.setopt(cu.URL, website_url)
        cu.setopt(cu.WRITEDATA, buffer)
        cu.perform()
        cu.close()
        self.body = buffer.getvalue()

    """
    Read JSON - GET Request only
    """
    def readbdd(self):
        jsonbody = json.loads(self.body.decode('iso-8859-1'))
        return jsonbody


class Settings:

    def __init__(self):
        pass

    def get_conf_setting(self, setting_path):
        return JsonManager(c.CONFIG_PATH + "settings.json").readjson()[setting_path]

    """
    Read JSON - GET Request only"""
    def get_bdd_settings(self, url, setting_path):
        return BDDManager(url).readbdd()[setting_path]
