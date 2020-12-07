import random
import math

DIR = [
    (0,0),
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (1,1),
    (1,-1),
    (-1,1),
    (-1,-1)
    ]

class Brain(object):
    def __init__(self, size):
        self.directions = [(0, 0)] * size
        self.size = size
        self.randomize()
        self.step = 0

    def randomize(self):
        for i in range(self.size):
            randomVar = math.floor(random.random() * 9)
            self.directions[i] = DIR[randomVar]


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
                randomVar = math.floor(random.random() * 5)
                self.directions[i] = DIR[randomVar]
