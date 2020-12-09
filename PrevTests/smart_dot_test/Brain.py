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
            randomAngle = random.random() * 2* math.pi
            self.directions[i] = (25 * math.cos(randomAngle), 25 * math.sin(randomAngle))


    def clone(self):
        clone = Brain(self.size)
        for i in range(self.size):
            clone.directions[i] = tuple(self.directions[i])

        return clone

    def mutate(self):
        mutationRate = 0.02
        for i in range(self.size):
            rand = random.random()
            if rand < mutationRate:
                randomAngle = random.random() * 2*math.pi
                self.directions[i] = (25 * math.cos(randomAngle), 25 * math.sin(randomAngle))


        
