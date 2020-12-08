from Brain import Brain
import operator
import math
import pygame

# BASED ON https://github.com/Code-Bullet/Smart-Dots-Genetic-Algorithm-Tutorial

# Dot class
class Dot(object):

    # Initialize necessary variables
    def __init__(self, w, h, brainsize):
        # Dot has brain and position
        self.brain = Brain(brainsize)
        self.brainsize = brainsize
        self.pos = (w, h)

        # Store initial position
        self.w = w
        self.h = h

        # Qualities of each dot
        self.dead = False
        self.reachedGoal = False
        self.isBest = False
        self.fitness = 0

    # Draw dot on screen
    def show(self, screen):

        # Color = red for alive, blue for best dot, gray for dead
        color = (255,0,0)

        if self.isBest:
            color = (0, 0, 255)
        elif self.dead:
            color = (100,100,100)

        pygame.draw.rect(screen, color, (self.pos[0]*15, self.pos[1]*15, 15, 15))


    # Move dot
    def move(self, walls):
        # Continue moving while moves exist in the brain
        if self.brain.size > self.brain.step:

            # Iterate through moves to change position
            currVal = self.brain.directions[self.brain.step]
            nextStep = tuple(map(operator.add, self.pos, currVal))

            # Only make move if there is no wall
            if nextStep not in walls:
                self.pos = nextStep
            self.brain.step += 1

        # Kill dot at end of brain directions
        else:
            self.dead = True

    # Update dot
    def update(self, goalx, goaly, walls, obstacle_pos):

        # Keep moving when alive and not at goal
        if not self.dead and not self.reachedGoal:

            # Kill dot if it reaches an obstacle
            if self.pos in obstacle_pos:
                self.dead = True

            self.move(walls)

            # Kill dot if it reaches an obstacle
            if self.pos in obstacle_pos:
                self.dead = True

            # Dot has reached goal
            elif self.pos[0] == goalx and self.pos[1] == goaly:
                self.reachedGoal = True

    # Calculate fitness function of dot
    def calculateFitness(self, goalx, goaly, path):
        # Fitness based on number of steps if dot succeeds
        # Add 1 to always be higher than a dot that does not arrive at goal
        if self.reachedGoal:
            self.fitness = 1 + 10000 /( self.brain.step * self.brain.step)

        # When dot is not at the goal
        else:
            # Find minimum distance of dot to best path from BFS
            min_dist = 10000
            index = -1
            for i in range(len(path)):
                dist = abs((self.pos[0] - path[i][0])) + abs((self.pos[1] - path[i][1]))
                if dist <= min_dist:
                    index = i
                    min_dist = dist

            # Fitness based on distance to path and how far along the path
            total_dist = min_dist + (len(path) - index) * 3
            self.fitness = 1/(total_dist * total_dist)

    # Make a baby dot by cloning it
    def makeBaby(self):
        baby = Dot(self.w, self.h, self.brainsize)
        baby.brain = self.brain.clone()
        return baby
