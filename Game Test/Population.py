from Dot import Dot
import random
import pygame
import pickle
import os
# BASED ON https://github.com/Code-Bullet/Smart-Dots-Genetic-Algorithm-Tutorial

# Population class to handle many dots
class Population(object):
    def __init__(self, size, startx, starty, goalx, goaly, brainsize, path):
        self.dots = []
        # Initialize array of dots
        for i in range(size):
            self.dots.append(Dot(startx,starty, brainsize))

        # Set values
        self.goalx = goalx
        self.goaly = goaly
        self.gen = 1
        self.bestDot = 0
        self.maxStep = brainsize
        self.fitnessSum = 0
        self.path = path

    # Draw dots on screen
    def show(self, screen):
        # Iterate through each dot on screen
        for dot in self.dots:
            dot.show(screen) 

        # Show best dot in blue
        self.dots[0].show(screen)

    # Update each dot in population
    def update(self, walls, obstacles):
        for dot in self.dots:
            # Kill dot if it oversteps 
            if dot.brain.step > self.maxStep:
                dot.dead = True
            # Update dot if within step limit
            else:
                dot.update(self.goalx, self.goaly, walls, obstacles)

    # Calculate fitness for each dot
    def calculateFitness(self):
        for dot in self.dots:
            dot.calculateFitness(self.goalx, self.goaly, self.path)

    # Check if every dot is dead in population
    def allDotsDead(self):
        for dot in self.dots:
            # Return false if a single dot is alive
            if not dot.dead and not dot.reachedGoal:
                return False
        return True

    # Regenerate next population
    def naturalSelection(self):
        # Create new array of dots
        newDots = []

        # Set best dot
        self.setBestDot()

        #Check total fitness
        self.calculateFitnessSum()

        # Always reproduce best dot
        newDots.append(self.dots[self.bestDot].makeBaby())
        newDots[0].isBest = True

        # Select a parent for every new dot and recreate it
        for i in range(len(self.dots) - 1):
            parent = self.selectParent()
            newDots.append(parent.makeBaby())

        # Set new generation of dots
        for i in range(len(self.dots)):
            self.dots[i] = newDots[i]

        # Increase generation
        self.gen += 1

        pygame.time.wait(50)

    # Save best dot to a .dat file
    def save(self, level):
        data = self.dots[0].brain.directions
        pickle.dump(data, open("data_" + str(level) + ".dat", "wb"))
        # print(data)

    # Load in the best dot into the first dot in population
    def upload(self, level):
        # loads saved data
        self.dots[0].brain.directions = pickle.load(open("data_" + str(level) + ".dat", "rb"))
        # print(self.dots[0].brain.directions)

    # Sum fitness of every dot in population
    def calculateFitnessSum(self):
        self.fitnessSum = 0
        for dot in self.dots:
            self.fitnessSum += dot.fitness
        # Print fitness sum for training verification
        print("Generation " + str(self.gen) + ": " + str(self.fitnessSum))

    # Select parent for any dot
    def selectParent(self):
        # Generate random number under total fitness sum
        rand = random.random() * self.fitnessSum
        runningSum = 0

        # Reproduce random dot, with more successful dots having proportionally higher chance
        for i in range(len(self.dots)):
            runningSum += self.dots[i].fitness
            if runningSum > rand:
                return self.dots[i]

        return self.dots[self.bestDot]

    # Motate every dot in population except the best
    def mutateBabies(self):
        for i in range(1, len(self.dots)):
            self.dots[i].brain.mutate()             ### does this stop best dot from mutating?

    # Find index of best dot in population
    def setBestDot(self):

        # Find dot with highest fitness function via linear search
        max = 0
        maxIndex = 0
        for i in range(len(self.dots)):
            if self.dots[i].fitness > max:
                max = self.dots[i].fitness
                maxIndex = i
      
        # Set bestDot value to index of best dot
        self.bestDot = maxIndex

        # Print steps for training tracking
        if self.dots[self.bestDot].reachedGoal:
            self.maxStep = self.dots[self.bestDot].brain.step
            print("step: " + str(self.maxStep))
