from Dot import Dot
import random
import pygame
import pickle
import os
import math

DIR = [
    (0,0),
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
    ]

# Population class for group of dots
class Population(object):
    def __init__(self, size, startx, starty, goalx, goaly, brainsize, path, train):
        self.dots = []
        # Create array of dots
        for i in range(size):
            self.dots.append(Dot(startx,starty, brainsize))

        # Set initial values
        self.goalx = goalx
        self.goaly = goaly
        self.gen = 1
        self.bestDot = 0
        if train:
            self.maxStep = 20
        else:
            self.maxStep = brainsize
        self.brainsize = brainsize
        self.fitnessSum = 0
        self.path = path

    # Draw every dot on screen
    def show(self, screen):
        for dot in self.dots:
            dot.show(screen)
        # Show best dot in blue
        self.dots[0].show(screen)

    # Update every dot 
    def update(self, walls, obstacles):
        # Kill dot if it exceeds the min step required
        for dot in self.dots:
            if dot.brain.step > self.maxStep:
                dot.dead = True

            # Update otherwise
            else:
                dot.update(self.goalx, self.goaly, walls, obstacles)

    # Calculate fitness of every dot in population
    def calculateFitness(self):
        for dot in self.dots:
            dot.calculateFitness(self.goalx, self.goaly, self.path)

    # Check if every dot is dead
    def allDotsDead(self):
        for dot in self.dots:
            # Return false if even one is alive
            if not dot.dead and not dot.reachedGoal:
                return False
        return True

    # Natural selection for population
    def naturalSelection(self):
        # Make array of new dots
        newDots = []
        # Find best dot and fitness sum
        self.setBestDot()
        self.calculateFitnessSum()

        # Best dot in population is carried over
        newDots.append(self.dots[self.bestDot].makeBaby())
        newDots[0].isBest = True

        # Find random parent for every subsequent dot
        # Make baby for each
        for i in range(len(self.dots) - 1):
            parent = self.selectParent()
            newDots.append(parent.makeBaby())

        # Set new population
        for i in range(len(self.dots)):
            self.dots[i] = newDots[i]

        # Increase generation
        self.gen += 1

        if self.gen % 30 == 0 and self.maxStep < self.brainsize:
            for dot in self.dots:
                for i in range(self.maxStep, self.brainsize):
                    r = math.floor(random.random() * 5) 
                    dot.brain.directions[i] = DIR[r]

            self.maxStep += 20

        pygame.time.wait(50)

    # Save directions from best dot
    def save(self, level):
        data = self.dots[0].brain.directions
        pickle.dump(data, open("data_" + str(level) + ".dat", "wb"))
        # print(data)

    # Upload data into best dot given a level
    def upload(self, level):
        # loads saved data
        self.dots[0].brain.directions = pickle.load(open("data_" + str(level) + ".dat", "rb"))
       #  print(self.dots[0].brain.directions)

    # Accessor for generation value
    def generation(self):
        gen = self.gen
        return gen

    # Sum fitness for entire population
    def calculateFitnessSum(self):
        self.fitnessSum = 0
        for dot in self.dots:
            self.fitnessSum += dot.fitness
        # Print for testing
        print("Generation " + str(self.gen) + ": " + str(self.fitnessSum))

    # Select parent for a baby
    def selectParent(self):
        # Create random number from 0 to fitnessSum
        rand = random.random() * self.fitnessSum
        runningSum = 0

        # Iterate through dots, higher fitness dots have higher chance to reproduce
        for i in range(len(self.dots)):
            runningSum += self.dots[i].fitness
            if runningSum > rand:
                return self.dots[i]

        return self.dots[self.bestDot]

    # Mutate every baby in dots except first one
    def mutateBabies(self):
        for i in range(1, len(self.dots)):
            self.dots[i].brain.mutate()

    # Find best dot
    def setBestDot(self):
        # Linear search for index of dot with highest fitness
        max = 0
        maxIndex = 0
        for i in range(len(self.dots)):
            if self.dots[i].fitness > max:
                max = self.dots[i].fitness
                maxIndex = i
        # Set value
        self.bestDot = maxIndex

        # Set new limit on steps if goal is reached
        if self.dots[self.bestDot].reachedGoal:
            self.maxStep = self.dots[self.bestDot].brain.step
            print("step: " + str(self.maxStep))
