from Brain import Brain
import operator
import math
import pygame

class Dot(object):
    def __init__(self, w, h, brainsize):
        self.brain = Brain(brainsize)
        self.brainsize = brainsize
        self.pos = (w/2, h/ 4 * 3)
        self.w = w
        self.h = h
        self.vel = (0,0)
        self.acc = (0,0)
        self.dead = False
        self.reachedGoal = False
        self.isBest = False
        self.fitness = 0
        self.dead_early = False

    def show(self, screen):
        color = (255,0,0)
        if self.isBest:
            color = (0, 255, 0)
        pygame.draw.rect(screen, color, (self.pos[0] - 10, self.pos[1] - 10, 20, 20))


    def pos_x(self):
        return round(self.pos[0])

    def pos_y(self):
        return round(self.pos[1])

    def move(self):
        if self.brain.size > self.brain.step:
            self.acc = self.brain.directions[self.brain.step]
            self.brain.step += 1
        else:
            self.dead = True

        self.vel = tuple(map(operator.add, self.vel, tuple(i / 2 for i in self.acc) ))
        mag = self.vel[0] * self.vel[0] + self.vel[1] * self.vel[1]
        if mag > 45:
            self.vel = tuple(i * 45 / mag for i in self.vel)
        self.pos = tuple(map(operator.add, self.pos, self.vel))
        
    def update(self, goalx, goaly):
        if not self.dead and not self.reachedGoal:
            self.move()
            if self.pos[0] < 2 or self.pos[1] < 2 or self.pos[0] > self.w-2 or self.pos[1] > self.h - 2:
                self.dead = True
                self.dead_early = True
            elif math.sqrt((goalx - self.pos[0]) * (goalx - self.pos[0]) + (goaly - self.pos[1]) * (goaly - self.pos[1])) < 15:
                self.reachedGoal = True
            elif self.pos[0] < 600 and self.pos[1] < 310 and self.pos[0] > 0 and self.pos[1] > 300:
                self.dead = True
                self.dead_early = True

    def calculateFitness(self, goalx, goaly):
        if self.reachedGoal:
            self.fitness = 1/16 + 10000 /( self.brain.step * self.brain.step)
        elif self.dead_early:
            self.fitness = -1
        else:
            dist = (goalx - self.pos[0]) * (goalx - self.pos[0]) + (goaly - self.pos[1]) * (goaly - self.pos[1])
            self.fitness = 1000/dist

    def makeBaby(self):
        baby = Dot(self.w, self.h, self.brainsize)
        baby.brain = self.brain.clone()
        return baby




