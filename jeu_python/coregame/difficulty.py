from coregame.gameobjects import key as key


class Facile:

    identifier = "F"

    def __init__(self):
        self.grille = key.EasyGrid()
        self.maxkey = 20
        self.keytimeout = 10
        self.courseurspeed = 1  # moins vite
        self.hitpenality = 15  # perd 15% de sa vitesse en heurtant une haie
        self.identifier = Facile.identifier


class Moyen:

    identifier = "M"

    def __init__(self):
        self.grille = key.MediumGrid()
        self.maxkey = 20
        self.keytimeout = 7
        self.courseurspeed = 0  # normal
        self.hitpenality = 35
        self.identifier = Moyen.identifier


class Difficile:

    identifier = "D"

    def __init__(self):
        self.grille = None
        self.maxkey = 15
        self.keytimeout = 3
        self.courseurspeed = -1  # plus vite
        self.hitpenality = 50
        self.identifier = Difficile.identifier
