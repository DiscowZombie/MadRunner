import os
import settings
import json

FILE_PATH = settings.PATH + "/user_statistics.json"


class UserStatistics:
    personnage = "gros"

    course = 0
    distance_walked = 0
    jump = 0

    best_score = 0
    worst_score = 0

    haie_break = 0
    letter_clicked = 0

    def __init__(self, personnage="gros", course=0, distance_walked=0, jump=0, best_score=0, worst_score=0,
                 haie_break=0,
                 letter_clicked=0):
        self.personnage = personnage
        self.course = course
        self.distance_walked = distance_walked
        self.jump = jump
        self.best_score = best_score
        self.worst_score = worst_score
        self.haie_break = haie_break
        self.letter_clicked = letter_clicked

    @staticmethod
    def loadfromfile():
        if not os.path.exists(settings.PATH):
            os.makedirs(settings.PATH)

        if not os.path.exists(FILE_PATH):
            return UserStatistics("gros")

        f = settings.JsonManager(FILE_PATH).readjson()
        personnage = f["personnage"]
        course = f["course"]
        distance_walked = f["distance_walked"]
        jump = f["jump"]
        best_score = f["best_score"]
        worst_score = f["worst_score"]
        haie_break = f["haie_break"]
        letter_clicked = f["letter_clicked"]

        return UserStatistics(personnage, course, distance_walked, jump, best_score, worst_score, haie_break,
                              letter_clicked)

    def savetofile(self):
        f = open(FILE_PATH, "w")
        f.write(json.dumps({
            "personnage": self.personnage,
            "course": self.course,
            "distance_walked": self.distance_walked,
            "jump": self.jump,
            "best_score": self.best_score,
            "worst_score": self.worst_score,
            "haie_break": self.haie_break,
            "letter_clicked": self.letter_clicked
        }))
        f.close()
