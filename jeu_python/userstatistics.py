import shelve


class UserStatistics:

    data = None
    stats = None

    def __init__(self):
        self.best_score = {
            "400m": None,
            "400m haie": None,
            "Course infinie": None
        }
        self.best_gm_score = {
            "400m": None,
            "400m haie": None,
            "Course infinie": None
        }
        self.score_total = 0
        self.nb_courses = 0
        self.nb_courses_echouees = 0
        self.nb_sauts = 0
        self.total_dist = 0
        self.correct_letters = 0
        self.wrong_letters = 0
        self.missed_letters = 0
        self.haies_traversees = 0
        self.haies_renversees = 0
        self.temps_jeu = 0

    def load(self):
        base = shelve.open("game_stats")

        if "stats_obj" in base:
            for attrname in self.__dict__:
                self.__setattr__(attrname, base["stats_obj"].__getattribute__(attrname))
        else:
            base["stats_obj"] = self

        UserStatistics.data = base
        UserStatistics.stats = self

    def save(self):
        UserStatistics.data["stats_obj"] = self
        UserStatistics.data.close()
        UserStatistics.data = shelve.open("game_stats")

    def set(self, statname, value, statname2=None):
        if statname2:
            self.__getattribute__(statname)[statname2] = value
        else:
            self.__setattr__(statname, value)

    def increment(self, statname, delta):
        self.__setattr__(statname, self.__getattribute__(statname) + delta)
