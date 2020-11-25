import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1200
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Worlds Hardest Game')

# .Rect(x-coord, y-coord, width, height)
player = pygame.Rect(50, 50, 30, 30)
goal = pygame.Rect(1100, 50, 50, 50)

# define common colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# define font
font = pygame.font.SysFont('Bauhaus 93', 60)

# show text on screen (this probs is not the best way to do this...)
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# fun background for later
# bg = pygame.image.load('img/space.jpg')

walls = [
pygame.Rect(0,0,20,screen_height),
pygame.Rect(0,0,screen_width, 20),
pygame.Rect(0, screen_height-20, screen_width, 20),
pygame.Rect(screen_width-20, 0, 20, screen_height),
pygame.Rect(screen_width/3, 0, 20, screen_height-200),
pygame.Rect(screen_width * 2/3, 200, 20, screen_height - 200)
]

class Obstacle(pygame.Rect):
    def __init__(self, x, y, width, height, vel):
        super().__init__(x, y, width, height)
        self.vel = vel
    def update(self):
        self.x += self.vel
        if self.right > screen_width * 2/3 or self.left < screen_width/3 + 20:
            self.vel = -self.vel

vel_left = 3
vel_right = -3

obstacles = [
    Obstacle(screen_width/3 + 20, 240, 30, 30, vel_left),
    Obstacle(screen_width/3 + 20, 360, 30, 30, vel_left),
    Obstacle(screen_width/3 + 20, 480, 30, 30, vel_left),
    Obstacle(screen_width * 2/3 - 50, 300, 30, 30, vel_right),
    Obstacle(screen_width * 2/3 - 50, 420, 30, 30, vel_right),
    Obstacle(screen_width * 2/3 - 50, 540, 30, 30, vel_right),
]

run = True
alive = True
win = False
while run:

    clock.tick(fps)

    #draw background
    # screen.blit(bg, (0,0))

    #delay start of game by 10ms
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # move player using arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.x < screen_width - 50:
        player.x += 5
    if keys[pygame.K_UP] and player.y > 0:
        player.y -= 5
    if keys[pygame.K_DOWN] and player.y < screen_height - 50:
        player.y += 5

    # collision with obstacle
    for obstacle in obstacles:
        obstacle.update()
        if player.colliderect(obstacle):
            alive = False

    # collision with wall
    for wall in walls:
        if player.colliderect(wall):
            alive = False

    if player.colliderect(goal):
        win = True

    screen.fill(black)

    if alive == True and win == False:
        pygame.draw.rect(screen, red, player)
        pygame.draw.rect(screen, blue, goal)

        for wall in walls:
            pygame.draw.rect(screen, white, wall)

        for obstacle in obstacles:
            pygame.draw.rect(screen, green, obstacle)

    else:
        if win:
            draw_text("You Win!", font, white, 500, 20)
        else:
            draw_text("Game over", font, white, 500, 20)

    pygame.display.update()

pygame.quit()
