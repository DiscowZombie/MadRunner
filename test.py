import settings
import constantes

valeur = settings.JsonManager(constantes.CONFIG_PATH+"settings.json").readJSON()["valeur"]
