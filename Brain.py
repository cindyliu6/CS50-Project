import random
import math

# BASED ON https://github.com/Code-Bullet/Smart-Dots-Genetic-Algorithm-Tutorial

# Possible directions for movement
DIR = [
    (0,0),
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
    ]

# Brain class
class Brain(object):

    # Initialize values
    def __init__(self, size):
        self.directions = [(0, 0)] * size
        self.size = size
        self.randomize()
        self.step = 0

    # Randomly generates steps for brain to go in
    def randomize(self):
        for i in range(self.size):
            randomVar = math.floor(random.random() * 5)
            self.directions[i] = DIR[randomVar]

    # Create a duplicate brain and return it
    def clone(self):
        clone = Brain(self.size)
        for i in range(self.size):
            clone.directions[i] = tuple(self.directions[i])

        return clone

    # Mutations for genetic algorithm
    def mutate(self):
        # Set mutation rate
        mutationRate = 0.02

        # Mutate to random values over time
        for i in range(self.size):
            rand = random.random()
            if rand < mutationRate:
                randomVar = math.floor(random.random() * 5)
                self.directions[i] = DIR[randomVar]
