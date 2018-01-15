import statemanager

class GameManager:

    def __init__(self):
        statemanager.StateManager.setstate(statemanager.StateEnum.PLAYING)
        self.walkingspeed = 1
        self.distance = 0

    def getdistance(self):
        return self.distance

    def walkspeed(self):
        return self.walkingspeed

    def increasedistance(self):
        self.distance += 1

    def setwalkingspeed(self, speed):
        self.walkingspeed = speed
