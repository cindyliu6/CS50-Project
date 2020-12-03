from Brain import Brain
import operator
import math
import pygame

class Dot(object):
    def __init__(self, w, h, brainsize):
        self.brain = Brain(brainsize)
        self.brainsize = brainsize
        self.pos = (w, h)
        self.w = w
        self.h = h
        self.dead = False
        self.reachedGoal = False
        self.isBest = False
        self.fitness = 0
        self.dead_early = False

    def show(self, screen):
        color = (255,0,0)

        if self.isBest:
            color = (0, 255, 0)
        pygame.draw.rect(screen, color, (self.pos[0]*15, self.pos[1]*15, 15, 15))


    # def pos_x(self):
    #     return round(self.pos[0])
    #
    # def pos_y(self):
    #     return round(self.pos[1])

    def move(self):
        if self.brain.size > self.brain.step:
            currVal = self.brain.directions[self.brain.step]
            self.brain.step += 1
        else:
            self.dead = True

        self.pos = tuple(map(operator.add, self.pos, currVal))

    def update(self, goalx, goaly, walls, obstacle_pos):
        if not self.dead and not self.reachedGoal:
            self.move()
            if self.pos in walls or self.pos in obstacle_pos:
                self.dead = True
                self.dead_early = True
            elif self.pos[0] == goalx and pos[1] == self.goaly:
                self.reachedGoal = True

    def calculateFitness(self, goalx, goaly):
        if self.reachedGoal:
            self.fitness = 1/16 + 10000 /( self.brain.step * self.brain.step)
        else:
            dist = (goalx - self.pos[0]) * (goalx - self.pos[0]) + (goaly - self.pos[1]) * (goaly - self.pos[1])
            self.fitness = 1/dist

    def makeBaby(self):
        baby = Dot(self.w, self.h, self.brainsize)
        baby.brain = self.brain.clone()
        return baby
