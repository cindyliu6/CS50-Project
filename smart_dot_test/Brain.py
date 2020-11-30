import random
import math

class Brain(object):
    def __init__(self, size):
        self.directions = [(0, 0)] * size
        self.size = size
        self.randomize()
        self.step = 0

    def randomize(self):
        for i in range(self.size):
            randomAngle = random.randrange(0, 1) * 2* math.pi
            self.directions[i] = (math.cos(randomAngle), math.sin(randomAngle))

    def clone(self):
        clone = Brain(self.size)
        for i in range(self.size):
            clone.directions[i] = self.directions[i]

        return clone

    def mutate(self):
        mutationrate = 0.01
        for i in range(self.size):
            rand = random.randrange(0,1)
            if rand < mutationRate:
                randomAngle = random.randrange(0, 2*math.pi)
                self.directions[i] = (math.cos(randomAngle), math.sin(randomAngle))


        
