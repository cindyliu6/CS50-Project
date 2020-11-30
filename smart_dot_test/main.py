import pygame
import Brain
import Dot
from Population import Population

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Worlds Hardest Game')

# .Rect(x-coord, y-coord, width, height)
# player = pygame.Rect(50, 50, 30, 30)
goal = pygame.Rect(600, 50, 50, 50)
wall = pygame.Rect(0, 300, 600, 10)

# define common colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

run = True
population = Population(100, 625, 75, 500)

while run:
	clock.tick(fps)
	pygame.time.delay(10)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	screen.fill(black)

	# pygame.draw.rect(screen, red, player)
	pygame.draw.rect(screen, blue, goal)
	pygame.draw.rect(screen, white, wall)
	pygame.time.wait(2)

	allDead = population.allDotsDead() ### do I have to pass in self? ### confused about calling functions from classes in diff files
	if allDead:
		population.calculateFitness()
		population.naturalSelection()
		population.mutateBabies()
	else:
		#for dot in population.dots:
		#	#print("(" + str(dot.pos_x()) + ", " + str(dot.pos_y()) + ") ")
		#	pygame.draw.rect(screen, red, (dot.pos_x(), dot.pos_y(), 20, 20))
		population.update()
		population.show(screen)

	pygame.display.update()
pygame.quit()
