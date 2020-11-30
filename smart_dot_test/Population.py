from Dot import Dot
import random

class Population(object):
    def __init__(self, size, goalx, goaly, brainsize):
        self.dots = []
        self.brainsize = brainsize
        for i in range(size):
            self.dots.append(Dot(800,600, self.brainsize))
        self.goalx = goalx
        self.goaly = goaly
        self.gen = 1
        self.bestDot = 0
        self.minStep = 1000
        self.fitnessSum = 0

    def show(self, screen):
        for dot in self.dots:
            dot.show(screen)

    def update(self):
        for dot in self.dots:
            if dot.brain.step > self.minStep:
                dot.dead = True
            else:
                dot.update(self.goalx, self.goaly)

    def calculateFitness(self):
        for dot in self.dots:
            dot.calculateFitness(self.goalx, self.goaly)
        
        print("COORDS---------------------------------------------------")
        print(self.goalx)
        print(self.goaly)

    def allDotsDead(self):
        for dot in self.dots:
            if not dot.dead and not dot.reachedGoal:
                return False
        return True

    def naturalSelection(self):
        newDots = []
        self.setBestDot()
        self.calculateFitnessSum()

        newDots.append(self.dots[self.bestDot].makeBaby())
        newDots[0].isBest = True

        for i in range(len(self.dots) - 1):
            parent = self.selectParent()
            newDots.append(parent.makeBaby())

        for i in range(len(self.dots)):
            self.dots[i] = newDots[i]
        self.gen += 1

    def calculateFitnessSum(self):
        for dot in self.dots:
            self.fitnessSum += dot.fitness

    def selectParent(self):
        rand = random.random() * self.fitnessSum - 1
        runningSum = 0

        for dot in self.dots:
            if (dot.fitness > 0):
                runningSum += dot.fitness

            else:
                runningSum += 0.001
            if runningSum > rand:
                return dot

        return self.dots[round(rand)]


    def mutateBabies(self):
        for dot in self.dots:
            dot.brain.mutate()

    def setBestDot(self):
        max = 0
        maxIndex = 0
        for i in range(len(self.dots)):
            if self.dots[i].fitness > max:
                max = self.dots[i].fitness
                maxIndex = i
                print("-----------------------BEST FOUND--------------------------")
            print(self.dots[i].fitness)

        bestDot = maxIndex

        if self.dots[bestDot].reachedGoal:
            self.minStep = self.dots[bestDot].brain.step
            print("step: " + self.minStep)
