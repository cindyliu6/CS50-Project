import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Worlds Hardest Game')

# .Rect(x-coord, y-coord, width, height)
player = pygame.Rect(50, 50, 30, 30)
goal = pygame.Rect(600, 50, 50, 50)

# define common colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

run = True
while run:
	clock.tick(fps)
	pygame.time.delay(10)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	screen.fill(black)

	pygame.draw.rect(screen, red, player)
	pygame.draw.rect(screen, blue, goal)

	pygame.display.update()
pygame.quit()
