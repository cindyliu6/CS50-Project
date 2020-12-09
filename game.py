import pygame
import numpy as np
import operator
import random
import pickle
import os
from Population import Population
from Pathfinder import find_path

# define dimensions
HEIGHT = 40
WIDTH = 60
SIZE = 15
screen_width = WIDTH * SIZE
screen_height = HEIGHT * SIZE + 50
START = (5, 5)
END = (50, 35)


# Five human playable levels
PLAY_LEVELS = 5


# define common colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


# Define direction tuples
DIR = {
	'u' : (0, -1), # north is -y
	'd' : (0, 1),
	'l' : (-1,0),
	'r' : (1,0)
	}


# Show text on screen
def draw_text(text, font, text_col, x, y, screen):
	# Create image for text and blit onto screen
	pygame.font.init()
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


# Drawing game surface and walls
def draw_grid(surface, walls):
	# Iterate over entire surface
	for y in range(0, HEIGHT):
		for x in range(0, WIDTH):
			# Create rectangle to draw on grid
			r = pygame.Rect((x * SIZE, y * SIZE), (SIZE, SIZE))
			# Walls are white, otherwise black
			if (x, y) in walls:
			   color = white
			else:
			   color = black
			pygame.draw.rect(surface, color, r)


# Create 2D array as board for path finding algorithm
def get_board(w, h, walls):
	board =[]
	for i in range(h):
		row = []
		for j in range(w):
			# j represents each column, i represents each row
			if (j, i) in walls:
				# -1 used for walls
				row.append(-1)
			else:
				row.append(0)
		# Add each row to board
		board.append(row)
	return board


# Moving obstacle class
class Obstacle():
	# Initialize values
	def __init__(self, x, y, xvel, yvel, x_bound, x_bound2, y_bound, y_bound2):
		self.xvel = xvel
		self.yvel = yvel
		self.position = (x, y)
		self.xlimit = (x_bound)
		self.xlimit2 = (x_bound2)
		self.ylimit = (y_bound)
		self.ylimit2 = (y_bound2)

	# Update position of obstacle
	def update(self):
		# Map position to next spot in x or y bound depending on velocity
		self.position = tuple(map(operator.add, self.position, (self.xvel, self.yvel)))
		# Flip velocity if reached bound
		if self.position[0] > self.xlimit or self.position[0] < self.xlimit2:
			self.xvel = -self.xvel
		if self.position[1] > self.ylimit or self.position[1] < self.ylimit2:
			self.yvel = -self.yvel

	# Draw obstacle on screen
	def draw(self, surface):
		# Create rectangle and draw on screen at appropriate square in grid
		r = pygame.Rect((self.position[0]*SIZE,self.position[1]*SIZE), (SIZE, SIZE))
		pygame.draw.rect(surface, green, r)

	# Return position of obstacle
	def get_position(self):
		return self.position


# Player class
class Player():

	# Initialize original position of player
	def __init__(self, x, y):
		self.position = (x, y)

	# Accessor
	def get_position(self):
		return self.position

	# Move in direction notated in move based on DIR array
	# Moves up, right, left, down based on dir
	def move(self, dir):
		self.position = tuple(map(operator.add, self.position, DIR[dir]))

	# Draw self on screen
	def draw(self, surface):
		r = pygame.Rect((self.position[0]*SIZE,self.position[1]*SIZE), (SIZE, SIZE))
		pygame.draw.rect(surface, red, r)

	# Check collisions between player and a set of walls
	def collisions(self, solids, x, y):
		for solid in solids:
			# Collides if there's wall in that direction
			if self.position[0] == solid[0] + x and self.position[1] == solid[1] + y:
				return True
		return False


# Goal class
class Goal():
	# Initialize a goal
	def __init__ (self, x, y):
		self.position = (x, y)

	# Draw goal on screen in blue
	def draw(self, surface):
		r = pygame.Rect((self.position[0]*SIZE,self.position[1]*SIZE), (SIZE, SIZE))
		pygame.draw.rect(surface, blue, r)

	# Return position of goal
	def get_position(self):
		return self.position


# Main function
def main():
	# Initialize pygame, clock, etc
	pygame.init()

	clock = pygame.time.Clock()
	fps = 60
	home_fps = 10

	pygame.display.set_caption('Worlds Hardest Game')
	
	# define fonts
	font = pygame.font.SysFont('Bauhaus 93', 70)
	homepage_font = pygame.font.SysFont('Bauhaus 93', 45)
	instruction_font = pygame.font.SysFont('Arial', 30)

	# Goal for each level
	goal = Goal(END[0], END[1])

	screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

	# Initialize default values for game
	run = True
	game = True	
	homepage = True
	gamemode = 0

	# Game runs
	while game:
		# Initialize homepage
		while homepage:
			clock.tick(home_fps)

			# Draw image and text for mode select screen
			image = pygame.image.load('res/homepage.jpg')
			# Draw circle on screen based on which gamemode is selected
			pygame.draw.ellipse(image, red, (230, 265 + gamemode * 60, 20, 20))
			draw_text("PLAY GAME", homepage_font, black, 280, 250, image)
			draw_text("TRAIN COMPUTER", homepage_font, black, 280, 310, image)
			draw_text("WATCH COMPUTER", homepage_font, black, 280, 370, image)

			screen.blit(image, (0,0))

			# End all loops if pygame closes
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					homepage = False
					game = False
					run = False

			# Toggle gamemode going up and down
			# 0 for play, 1 for train, 2 for watch
			keys = pygame.key.get_pressed()

			# Use mod3 to shift between 0, 1, 2 
			if keys[pygame.K_UP]:
				gamemode = (gamemode - 1) % 3
			elif keys[pygame.K_DOWN]:
				gamemode = (gamemode + 1) % 3

			# Press right key or enter to continue
			elif keys[pygame.K_RIGHT] or keys[pygame.K_RETURN]:
				homepage = False

			pygame.display.update()


		# HUMAN PLAYER
		if gamemode == 0:
			# Initialize level at 1, start game as alive with no win
			level = 1
			alive = True
			win = False

			# Reinitialize run as True if player leaves and comes back
			run = True

			# Iterate through each level
			while level <= PLAY_LEVELS:
				# Open level
				player = Player (START[0], START[1])
				obstacles = pickle.load(open("level_data/obs_" + str(level) + ".dat", "rb"))
				walls = pickle.load(open("level_data/walls_" + str(level) + ".dat", "rb"))

				# Run each level
				while run:

					# Tick clock at standard fps
					clock.tick(fps)
					
					# Break all loops if pygame quits
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							level = 100
							run = False

					# If player is still alive and has not won, let them move
					if alive == True and win == False:
						
						# Draw black screen (reset background)
						pygame.draw.rect(screen, black, pygame.Rect(0,0, screen_width, screen_height))

						# Move player using arrow keys
						move = pygame.key.get_pressed()
						if move[pygame.K_LEFT] and not player.collisions(walls, 1, 0):
							player.move('l')
						elif move[pygame.K_RIGHT] and not player.collisions(walls, -1, 0):
							player.move('r')

						# Allows for diagonal movement if two directional keys are pressed
						# Opposite keys not at same time
						if move[pygame.K_UP] and not player.collisions(walls, 0, 1):
							player.move('u')
						elif move[pygame.K_DOWN] and not player.collisions(walls, 0, -1):
							player.move('d')

						# If player moves into an obstacle, the player dies
						for i in range(len(obstacles[0])):
							if player.get_position() == obstacles[0][i].get_position():
								alive = False

						# Draw everything onto screen
						draw_grid(screen, walls)
						goal.draw(screen)
						player.draw(screen)

						# Update every obstacle
						for i in range(len(obstacles[0])):
							obstacles[0][i].update()
							obstacles[0][i].draw(screen)
							# If obstacle hits player, then player dies
							# This prevents some skipping over 
							# (bug occured if obstacles are not checked both before and after player movement)
							if player.get_position() == obstacles[0][i].get_position():
								alive = False

						# Player wins if they reach goal
						if player.get_position() == goal.get_position():
							win = True

					# Either player is dead or player won
					else:
						# If player wins, draw winner text and increment level
						if win:
							draw_text("You Win!", font, white, 450, 20, screen)
							win = False
							level += 1
						# Restart level if player dies
						else:
							draw_text("Try Again", font, white, 450, 20, screen)
							alive = True

						pygame.display.update()
						pygame.time.wait(1000)
						break

					# Instruction text at bottom
					draw_text("Press R to restart level", instruction_font, white, 50, 605, screen)
					draw_text("Press H to go to home screen", instruction_font, white, 400, 605, screen)

					pygame.display.update()

					# Restarts current level with R
					if move[pygame.K_r]:
						break
					# Back to homepage with H
					elif move[pygame.K_h]:
						homepage = True
						run = False

				# Quit out if not running
				if not run:
					level = 100
					if not homepage:
						pygame.quit()

			## Once the player beats level 5, return to homepage
			homepage = True

		# Computer run mode
		# Only 3 computer trained levels
		else:
			# Open up level select screen and reinitialize run if needed
			levelSelect = True
			level = 0
			run = True

			# Level select screen
			while levelSelect:
				clock.tick(home_fps)

				# Open up level select screen
				image = pygame.image.load('res/level_select.jpg')
				# Draw ellipse based on selected level
				pygame.draw.ellipse(image, red, (230, 265 + level * 60, 20, 20))
				draw_text("LEVEL 1", homepage_font, black, 280, 250, image)
				draw_text("LEVEL 2", homepage_font, black, 280, 310, image)
				draw_text("LEVEL 3", homepage_font, black, 280, 370, image)

				screen.blit(image, (0,0))

				# Quit out of game by breaking all loops
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						run = False
						levelSelect = False
						game = False
						break

				# Allow selection of level using mod3
				keys = pygame.key.get_pressed()
				if keys[pygame.K_UP]:
					level = (level - 1) % 3
				elif keys[pygame.K_DOWN]:
					level = (level + 1) % 3
				# Select level with right key or enter
				elif keys[pygame.K_RIGHT] or keys[pygame.K_RETURN]:
					# Go from 0-2 to 1-3 for levels
					level += 1
					levelSelect = False
					
				pygame.display.update()
			
			# Break out of loop if needed
			if not game:
				break

			# Otherwise, open up data for the level and find the best path 
			walls = pickle.load(open("level_data/walls_" + str(level) + ".dat", "rb"))
			obstacles = pickle.load(open("level_data/obs_" + str(level) + ".dat", "rb"))
			board = get_board(WIDTH, HEIGHT, walls)
			path = find_path(board, START, END, level)

			# If in training mode
			if gamemode == 1:
				# Initialize population of 100 to train with the given path as reward
				population = Population(100, START[0], START[1], END[0], END[1], 500, path, True)

				# If training needed to be spread out over time this can be uncommented
				# population.upload(level)

			# If in watch mode, load in a saved model for the level
			elif gamemode == 2:
				population = Population(1, START[0], START[1], END[0], END[1], 500, path, False)
				population.upload(level)

			# Loop while game runs
			while run:
				clock.tick(fps)

				# Refresh background
				pygame.draw.rect(screen, black, pygame.Rect(0,0, screen_width, screen_height))

				#delay start of game by 10ms
				pygame.time.delay(10)

				# Quit out by breaking loops
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						run = False

				# Draw board and goal onto screen
				draw_grid(screen, walls)
				goal.draw(screen)

				# Write instruction
				draw_text("Press H to go to home screen", instruction_font, white, 50, 605, screen)

				# Update and draw obstacles onto screen
				# Population will check before and after each dot moves for collisions to prevent "skip over" bug
				for i in range(len(obstacles[0])):
					obstacles[0][i].update()
					obstacles[0][i].draw(screen)
					obstacles[1][i] = obstacles[0][i].get_position()

				# Delay to animate
				pygame.time.wait(1)

				# Training mode
				if gamemode == 1:

					# Print out generation
					gen = population.generation()
					draw_text("Generation: " + str(gen), instruction_font, white, 620, 605, screen)

					# Check if dots are all dead in population
					allDead = population.allDotsDead()
					# When all dots are dead
					if allDead:
						# Calculate fitness and select next generation
						population.calculateFitness()
						population.naturalSelection()
						## Uncomment this line to save training data
						# population.save(level)

						# Mutate babies
						population.mutateBabies()

						# Reset level
						obstacles = pickle.load(open("level_data/obs_" + str(level) + ".dat", "rb"))

					# Update dots as normal if one is still alive
					# Array obstacles[1] is to allow Population.py to treat this as tuples, not Obstacles
					# Only cares about positions
					else:
						population.update(walls, obstacles[1])
						population.show(screen)

				# Watch mode
				if gamemode == 2:
					# Update every step for population
					population.update(walls, obstacles[1])
					population.show(screen)

				pygame.display.update()

				# Break out of game if pressing H
				keys = pygame.key.get_pressed()
				if keys[pygame.K_h]:
					homepage = True
					break

				if not run:
					pygame.quit()
		if not game:
			pygame.quit()

# Run main
if __name__ == "__main__":
	main()
