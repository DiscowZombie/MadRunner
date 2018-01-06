from threading import Thread

class View(Thread):

    def __init__(self,pygame):
        Thread.__init__(self)
        self.pygame = pygame
        self.queue = []

    def run(self):
        pygame = self.pygame
        while True: #bon, il faut normalement obtenir le state du jeu !
            pygame.display.flip()
            for functable in self.queue:
                functable[0](*functable[1])

            self.queue.clear()

    def WaitFlip(self,func,*args):
        self.queue.append([func,args])

        # je sais pas comment attendre que ça fasse le flip !
