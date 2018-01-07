import toolbox
import functions

class View:

    def __init__(self):
        print("setup view")

    def mousebutton1down(self,position): # click gauche
        boutons = toolbox.Button.getButtons(self)
        for bouton in boutons:
            bouton.mousein = functions.checkmousebouton(position, bouton.x, bouton.y, bouton.width, bouton.height)

    def mousebutton1up(self,position):
        print("plus en train de click")
