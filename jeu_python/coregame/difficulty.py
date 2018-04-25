from coregame.gameobjects import key as key


class Facile:

    def __init__(self):
        self.grille = key.EasyGrid()
        self.maxkey = 20
        self.keytimeout = 10
        self.courseurspeed = 1  # moins vite
        self.hitpenality = 15  # perd 15% de sa vitesse en heurtant une haie


class Moyen:

    def __init__(self):
        self.grille = key.MediumGrid()
        self.maxkey = 20
        self.keytimeout = 7
        self.courseurspeed = 0  # normal
        self.hitpenality = 35


class Difficile:

    def __init__(self):
        self.grille = None
        self.maxkey = 15
        self.keytimeout = 3
        self.courseurspeed = -1  # plus vite
        self.hitpenality = 50
