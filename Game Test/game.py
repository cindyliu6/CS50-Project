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
screen_height = HEIGHT * SIZE
START = (5, 5)
END = (50, 35)

# define common colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# show text on screen (this probs is not the best way to do this...)
def draw_text(text, font, text_col, x, y, screen):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# fun background for later
# bg = pygame.image.load('img/space.jpg')

DIR = {
	'u' : (0, -1), # north is -y
	'd' : (0, 1),
	'l' : (-1,0),
	'r' : (1,0)
	}

# drawing game surface
def draw_grid(surface, walls, path):
	for y in range(0, HEIGHT):
		for x in range(0, WIDTH):
			r = pygame.Rect((x * SIZE, y * SIZE), (SIZE, SIZE))
			if (x, y) in walls:
			   color = (255,255,255)
			elif (x,y) in path:
				color = (0, 255, 255)
			else:
			   color = (0,0,0)
			pygame.draw.rect(surface, color, r)

def get_board(w, h, walls):
	board =[]
	for i in range(h):
		row = []
		for j in range(w):
			if (j, i) in walls:
				row.append(-1)
			else:
				row.append(0)
		board.append(row)
	return board

# moving obstacle class
class Obstacle():
	def __init__(self, x, y, xvel, yvel, x_bound, x_bound2, y_bound, y_bound2):
		self.xvel = xvel
		self.yvel = yvel
		self.position = (x, y)
		self.xlimit = (x_bound)
		self.xlimit2 = (x_bound2)
		self.ylimit = (y_bound)
		self.ylimit2 = (y_bound2)

	def update(self):
		self.position = tuple(map(operator.add, self.position, (self.xvel, self.yvel)))
		if self.position[0] > self.xlimit or self.position[0] < self.xlimit2:
			self.xvel = -self.xvel
		if self.position[1] > self.ylimit or self.position[1] < self.ylimit2:
			self.yvel = -self.yvel

	def draw(self, surface):
		r = pygame.Rect((self.position[0]*SIZE,self.position[1]*SIZE), (SIZE, SIZE))
		pygame.draw.rect(surface, green, r)

	def get_position(self):
		return self.position

# player class
class Player():

	def __init__(self, x, y):
		self.position = (x, y)
		pass

	def get_position(self):
		return self.position

	def set_position(self, x, y):
		self.position = (x, y)

	def move(self, dir):
		self.position = tuple(map(operator.add, self.position, DIR[dir]))

	def draw(self, surface):
		r = pygame.Rect((self.position[0]*SIZE,self.position[1]*SIZE), (SIZE, SIZE))
		pygame.draw.rect(surface, red, r)

# goal class
class Goal():
	def __init__ (self, x, y):
		self.position = (x, y)

	def draw(self, surface):
		r = pygame.Rect((self.position[0]*SIZE,self.position[1]*SIZE), (SIZE, SIZE))
		pygame.draw.rect(surface, blue, r)

	def get_position(self):
		return self.position


def main():
	pygame.init()

	clock = pygame.time.Clock()
	fps = 20

	walls = pickle.load(open("Game Test/level_data/walls_1.dat", "rb"))
	#walls = []

	#for x in range(WIDTH):
	#	walls.append((x, 0))
	#	walls.append((x, HEIGHT-1))

	#for x in range(HEIGHT):
	#	walls.append((0, x))
	#	walls.append((WIDTH-1, x))

	#for x in range(HEIGHT-10):
	#	walls.append((18, x))

	#for x in range(10, HEIGHT):
	#	walls.append((42, x))

	screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
	pygame.display.set_caption('Worlds Hardest Game')


	goal = Goal(END[0], END[1])

	vel_left = 1
	vel_right = -1

	obstacles = pickle.load(open("Game Test/level_data/obs_1.dat", "rb"))

	#obstacles = [[
	#		Obstacle(31, 11, vel_left),
	#		Obstacle(32, 12, vel_left),
	#		Obstacle(33, 13, vel_left),
	#		Obstacle(34, 14, vel_right),
	#		Obstacle(35, 15, vel_right),
	#		Obstacle(36, 16, vel_right)
	#	],
	#	[
	#		(31, 11),
	#		(32,12),
	#		(33,13),
	#		(34,14),
	#		(35,15),
	#		(36,16)
	#		]
	#]

	# define font
	font = pygame.font.SysFont('Bauhaus 93', 60)
	homepage_font = pygame.font.SysFont('Bauhaus 93', 45)

	homepage = True
	gamemode = 0

	board = get_board(WIDTH, HEIGHT, walls)
	path = find_path(board, START, END)
	# print(path)


	while homepage:
		clock.tick(fps)


		image = pygame.image.load('Game Test/homepage2.jpg')
		pygame.draw.ellipse(image, red, (230, 265 + gamemode * 60, 20, 20))
		draw_text("PLAY GAME", homepage_font, black, 280, 250, image)
		draw_text("TRAIN COMPUTER", homepage_font, black, 280, 310, image)
		draw_text("WATCH COMPUTER", homepage_font, black, 280, 370, image)

		screen.blit(image, (0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			gamemode = (gamemode - 1) % 3
		elif keys[pygame.K_DOWN]:
			gamemode = (gamemode + 1) % 3
		elif keys[pygame.K_RIGHT] or keys[pygame.K_RETURN]:
			homepage = False

		pygame.display.update()
		# print (gamemode)

	if gamemode == 0:

		def collisions(solids, x, y):
			for solid in solids:
				if player.get_position()[0] == solid[0] + x and player.get_position()[1] == solid[1] + y:
						# print("collision")
						return True
			return False

		level = 1
		run = True
		alive = True
		win = False

		while level < 3:
			player = Player (5,5)
			obstacles = pickle.load(open("Game Test/level_data/obs_" + str(level) + ".dat", "rb"))
			walls = pickle.load(open("Game Test/level_data/walls_" + str(level) + ".dat", "rb"))
			board = get_board(WIDTH, HEIGHT, walls)
			path = find_path(board, START, END)
			print(level)

			while run:
				clock.tick(fps)

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						level = 100
						run = False

				if alive == True and win == False:

					# move player using arrow keys
					move = pygame.key.get_pressed()
					if move[pygame.K_LEFT] and not collisions(walls, 1, 0):
						player.move('l')
					if move[pygame.K_RIGHT] and not collisions(walls, -1, 0):
						player.move('r')
					if move[pygame.K_UP] and not collisions(walls, 0, 1):
						player.move('u')
					if move[pygame.K_DOWN] and not collisions(walls, 0, -1):
						player.move('d')

					for i in range(len(obstacles[0])):
						if player.get_position() == obstacles[0][i].get_position():
							alive = False

					draw_grid(screen, walls, path)
					goal.draw(screen)
					player.draw(screen)

					for i in range(len(obstacles[0])):
						obstacles[0][i].update()
						obstacles[0][i].draw(screen)
						if player.get_position() == obstacles[0][i].get_position():
							alive = False

					if player.get_position() == goal.get_position():
						win = True

				else:
					if win:
						draw_text("You Win!", font, white, 500, 20, screen)
						win = False
						level += 1
					else:
						draw_text("Try Again", font, white, 500, 20, screen)
						alive = True
						
					pygame.display.update()
					pygame.time.wait(1000)
					break

				pygame.display.update()
				if not run:
					level = 100
					pygame.quit()




	else:
		if gamemode == 1:
			population = Population(100, START[0], START[1], END[0], END[1], 1000, path)

		elif gamemode == 2:
			population = Population(1, START[0], START[1], END[0], END[1], 1000, path)
			population.upload()

		while run:
			clock.tick(fps)

			#delay start of game by 10ms
			pygame.time.delay(10)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

			draw_grid(screen, walls, path)
			goal.draw(screen)

			for i in range(len(obstacles[0])):
				obstacles[0][i].update()
				obstacles[0][i].draw(screen)
				obstacles[1][i] = obstacles[0][i].get_position()

			pygame.time.wait(1)

			if gamemode == 1:
				allDead = population.allDotsDead()
				if allDead:
					population.calculateFitness()
					population.naturalSelection()
					# population.save()
					population.mutateBabies()
				else:
					population.update(walls, obstacles[1])
					population.show(screen)

			if gamemode == 2:
				population.update(walls, obstacles[1])
				population.show(screen)

			#print("update")
			pygame.display.update()

			if not run:
				pygame.quit()

if __name__ == "__main__":
	main()
