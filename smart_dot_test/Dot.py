from Brain import Brain
import operator
import math
import pygame

class Dot(object):
    def __init__(self, w, h):
        self.brain = Brain(1000)
        self.pos = (w/2, h/ 4 * 3)
        self.w = w
        self.h = h
        self.vel = (0,0)
        self.acc = (0,0)
        self.dead = False
        self.reachedGoal = False
        self.isBest = False
        self.fitness = 0

    def show(self, screen):
        pygame.draw.rect(screen, (255,0,0), (self.pos[0] - 10, self.pos[1] - 10, 20, 20))


    def pos_x(self):
        return round(self.pos[0])

    def pos_y(self):
        return round(self.pos[1])

    def move(self):
        if self.brain.size > self.brain.step:
            self.acc = self.brain.directions[self.brain.step]
        else:
            self.dead = True

        self.vel = tuple(map(operator.add, self.vel, self.acc))
        mag = self.vel[0] * self.vel[0] + self.vel[1] * self.vel[1]
        if mag > 10:
            self.vel = tuple(i * 10 / mag for i in self.vel)
        self.pos = tuple(map(operator.add, self.pos, self.vel))
        
    def update(self, goalx, goaly):
        if not self.dead and not self.reachedGoal:
            self.move()
            if self.pos[0] < 2 or self.pos[1] < 2 or self.pos[0] > self.w-2 or self.pos[1] > self.h - 2:
                self.dead = True
            elif math.sqrt((goalx - self.pos[0]) * (goalx - self.pos[0]) + (goaly - self.pos[1]) * (goaly - self.pos[1])) < 5:
                self.reachedGoal = True
            elif self.pos[0] < 600 and self.pos[1] < 310 and self.pos[0] > 0 and self.pos[1] > 300:
                self.dead = True

    def calculateFitness(self, goalx, goaly):
        if self.reachedGoal:
            self.fitness = 1/16 + 10000 * self.brain.step * self.brain.step
        else:
            dist = (goalx - self.pos[0]) * (goalx - self.pos[0]) + (goaly - self.pos[1]) * (goaly - self.pos[1])
            self.fitness = 1/dist

    def makeBaby(self):
        baby = Dot(self.w, self.h)
        baby.brain = self.brain.clone()
        return baby




