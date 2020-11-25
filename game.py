import pygame
import numpy as np

# define dimensions
HEIGHT = 40
WIDTH = 60
SIZE = 20
screen_width = WIDTH * SIZE
screen_height = HEIGHT * SIZE

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
    'u' : [0, -1], # north is -y
    'd' : [0, 1],
    'l' : [-1,0],
    'r' : [1,0]
    }

def draw_grid(surface):
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            r = pygame.Rect((x * SIZE, y * SIZE), (SIZE, SIZE))
            if (x+y) % 2 == 0:
               color = (255,255,255)
            else:
               color = (200,200,200)
            pygame.draw.rect(surface, (255,255,255), r)

class Obstacle(object):
    def __init__(self, x, y, vel):
        self.vel = vel
        self.position = [x, y]

    def update(self):
        self.position[0] += self.vel
        if self.position[0] > 40 or self.position[0] < 20:
            self.vel = -self.vel

    def draw(self, surface):
        r = pygame.Rect((self.position[0]*SIZE,self.position[1]*SIZE), (SIZE, SIZE))
        pygame.draw.rect(surface, green, r)

class Player(object):

    def __init__(self, x, y):
        self.position = [x, y]
        pass

    def get_position(self):
        return self.position

    def set_position(self, x, y):
        self.position = [x, y]
    
    def move(self, dir):
        self.position[0] = self.position[0] + DIR[dir][0]                                                       
        self.position[1] = self.position[1] + DIR[dir][1]

    def draw(self, surface):
        r = pygame.Rect((self.position[0]*SIZE,self.position[1]*SIZE), (SIZE, SIZE))
        pygame.draw.rect(surface, red, r)
    
class Agent():
    def __init__(self):
        super().__init__()
    def make_move():
        i = int(np.random().random() * 4)


def main():
    pygame.init()

    clock = pygame.time.Clock()
    fps = 20

    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    pygame.display.set_caption('Worlds Hardest Game')

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)

    player = Player(5, 5)

    walls = [
        pygame.Rect(0,0,20,screen_height),
        pygame.Rect(0,0,screen_width, 20),
        pygame.Rect(0, screen_height-20, screen_width, 20),
        pygame.Rect(screen_width-20, 0, 20, screen_height),
        pygame.Rect(screen_width/3, 0, 20, screen_height-200),
        pygame.Rect(screen_width * 2/3, 200, 20, screen_height - 200)
    ]
    
    vel_left = 1
    vel_right = -1

    obstacles = [
        Obstacle(31, 11, vel_left),
        Obstacle(32, 12, vel_left),
        Obstacle(33, 13, vel_left),
        Obstacle(34, 14, vel_right),
        Obstacle(35, 15, vel_right),
        Obstacle(36, 16, vel_right),
    ]

    # define font
    font = pygame.font.SysFont('Bauhaus 93', 60)

    # .Rect(x-coord, y-coord, width, height)
    #player = pygame.Rect(50, 50, 30, 30)
    goal = pygame.Rect(1100, 50, 50, 50)

    run = True
    alive = True
    win = False

    while run:  
        clock.tick(fps)

        #draw background
        # screen.blit(bg, (0,0))

        #delay start of game by 10ms
        pygame.time.delay(10)

        draw_grid(surface)
        player.draw(surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # move player using arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.get_position()[0] > 0:
            player.move('l')
        if keys[pygame.K_RIGHT] and player.get_position()[0] < WIDTH - 1:
            player.move('r')
        if keys[pygame.K_UP] and player.get_position()[1] > 0:
            player.move('u')
        if keys[pygame.K_DOWN] and player.get_position()[1] < HEIGHT - 1:
            player.move('d')

        ## collision with obstacle
        for obstacle in obstacles:
            obstacle.update()
        #    if player.colliderect(obstacle):
        #        alive = False

        ## collision with wall
        #for wall in walls:
        #    if player.colliderect(wall):
        #        alive = False

        #if player.colliderect(goal):
        #    win = True

        screen.fill(black)

        #if alive == True and win == False:
        #    #pygame.draw.rect(screen, red, player)
        #    pygame.draw.rect(screen, blue, goal)

        #    for wall in walls:
        #        pygame.draw.rect(screen, white, wall)

        for obstacle in obstacles:
            obstacle.draw(surface)

        #else:
        #    if win:
        #        draw_text("You Win!", font, white, 500, 20, screen)
        #    else:
        #        draw_text("Game Over", font, white, 500, 20, screen)
        
        screen.blit(surface, (0,0))
        pygame.display.update()
        if not run:
            pygame.quit()

if __name__ == "__main__":
    main()