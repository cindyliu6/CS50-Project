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
            color = (0, 0, 255)
        elif self.dead:
            color = (100,100,100)

        pygame.draw.rect(screen, color, (self.pos[0]*15, self.pos[1]*15, 15, 15))


    # def pos_x(self):
    #     return round(self.pos[0])
    #
    # def pos_y(self):
    #     return round(self.pos[1])

    def move(self, walls):
        if self.brain.size > self.brain.step:
            currVal = self.brain.directions[self.brain.step] 
            nextStep = tuple(map(operator.add, self.pos, currVal))
            if nextStep not in walls:
                self.pos = nextStep
            self.brain.step += 1
        else:
            self.dead = True

    def update(self, goalx, goaly, walls, obstacle_pos):
        if not self.dead and not self.reachedGoal:
            self.move(walls)
            if self.pos in obstacle_pos:
                self.dead = True
                self.dead_early = True
            elif self.pos[0] == goalx and self.pos[1] == goaly:
                self.reachedGoal = True

    def calculateFitness(self, goalx, goaly, path):
        if self.reachedGoal:
            self.fitness = 1 + 10000 /( self.brain.step * self.brain.step)
        else:
            min_dist = 10000
            index = -1
            for i in range(len(path)):
                dist = abs((self.pos[0] - path[i][0])) + abs((self.pos[1] - path[i][1]))
                if dist <= min_dist:
                    index = i
                    min_dist = dist

            total_dist = min_dist + (len(path) - index) * 3
            self.fitness = 1/(total_dist * total_dist)
            #if self.dead_early:
            #    self.fitness *= 0.8

    def makeBaby(self):
        baby = Dot(self.w, self.h, self.brainsize)
        baby.brain = self.brain.clone()
        return baby
