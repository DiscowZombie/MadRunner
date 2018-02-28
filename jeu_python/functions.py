import uielements.text as text
import uielements.surface as surface
import uielements.button as button
import uielements.image as image
import uielements.checkbox as checkbox


def centretexte(textsize, espace):  # Utilitaire pour center un texte ! Retourne la position x et y du texte
    return int(espace[0] / 2 - textsize[0] / 2), int(espace[1] / 2 - textsize[1] / 2)


def checkmousebouton(mousepos, buttonx, buttony, buttonwidth,
                     buttonheight):  # Utilitaire pour savoir si la souris se trouve dedans un bouton
    posx, posy = mousepos[0], mousepos[1]
    minx, maxx = buttonx, buttonx + buttonwidth
    miny, maxy = buttony, buttony + buttonheight
    if posx >= minx and posx <= maxx and posy >= miny and posy <= maxy:
        return True
    return False


def delete_menu_obj():
    for bouton in list(button.Button.boutons):
        bouton.__del__()
    for surf in list(surface.Surface.getSurfaces()):
        surf.__del__()
    for txt in list(text.Text.getTexts()):
        txt.__del__()
    for check in list(checkbox.Checkbox.getCheckboxes()):
        check.__del__()


def click_clavier(event):
    print('== > Evenement : ', event.type)
    for k, v in event.dict.items():
        print(k, v)
    print()


def isvalidint(supposedint):
    var = True if (supposedint is not None and int(supposedint) is not None) else False
    return var


def cartepathbyname(name=None):
    if name == "foret":
        return "foret"
    elif name == "athenes":
        return "athenes"
    else:
        return "jeux_olympiques"


def modejeubyname(modejeu=None):
    if modejeu == "400m":
        return "400m"
    elif modejeu == "400mh":
        return "400m_haie"
    else:
        return "infinie"


def difficultybyname(diff=1):
    if diff == 3:
        return "hard"
    elif diff == 2:
        return "normal"
    else:
        return "easy"
