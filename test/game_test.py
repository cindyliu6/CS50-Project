import pygame
import numpy as np
import operator
import random
from agent import Agent 

from keras.utils import to_categorical

# define dimensions
HEIGHT = 40
WIDTH = 60
SIZE = 15
screen_width = WIDTH * SIZE
screen_height = HEIGHT * SIZE

# define common colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#################################
#   Define parameters manually  #
#################################
def define_parameters():
    params = dict()
    # Neural Network
    params['epsilon_decay_linear'] = 1/75
    params['learning_rate'] = 0.0005
    params['first_layer_size'] = 50   # neurons in the first layer
    params['second_layer_size'] = 300   # neurons in the second layer
    params['third_layer_size'] = 50    # neurons in the third layer
    params['episodes'] = 150           
    params['memory_size'] = 2500
    params['batch_size'] = 1000
    # Settings
    params['weights_path'] = 'weights.hdf5'
    params['load_weights'] = False
    params['train'] = True
    params['plot_score'] = True
    return params

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

# moving obstacle class
class Obstacle():
    def __init__(self, x, y, vel):
        self.vel = vel
        self.position = (x, y)

    def update(self):
        self.position = tuple(map(operator.add, self.position, (self.vel, 0)))
        if self.position[0] > 40 or self.position[0] < 20:
            self.vel = -self.vel

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

# ai agent class
class AI_Player():
    def __init__(self, x, y):
        self.player = Player(x,y);

    def move(self, act):
        if len(act):
            if np.array_equal(act, [1, 0, 0,0]):
                self.player.move('l')
            elif np.array_equal(act, [0, 1, 0,0]):
                self.player.move('r')
            elif np.array_equal(act, [0, 0,1,0]):
                self.player.move('u')
            else:
                self.player.move('d')
        else:
            i = random.randint(0, 4)
            if i == 0:
                self.player.move('l')
            elif i == 1:
                self.player.move('r')
            elif i == 2:
                self.player.move('u')
            else:
                self.player.move('d')

    def get_position(self):
        return self.player.get_position()

    def draw(self, surface):
        self.player.draw(surface)

# ------------------------------------------RELEVANT WORK BELOW ----------------------------------------
# ------------------------------------------RELEVANT WORK BELOW ----------------------------------------
# ------------------------------------------RELEVANT WORK BELOW ----------------------------------------
# ------------------------------------------RELEVANT WORK BELOW ----------------------------------------
# ------------------------------------------RELEVANT WORK BELOW ----------------------------------------
# ------------------------------------------RELEVANT WORK BELOW ----------------------------------------
# ------------------------------------------RELEVANT WORK BELOW ----------------------------------------
# ------------------------------------------RELEVANT WORK BELOW ----------------------------------------
# ------------------------------------------RELEVANT WORK BELOW ----------------------------------------

class Game():
    def __init__(self, walls, obstacles, goal):
        self.player = AI_Player(5, 5)
        self.walls = walls
        self.goal = goal
        self.obstacles = obstacles
        self.obstacle_positions = []
        for obstacle in obstacles:
            self.obstacle_positions.append((obstacle.get_position()))
        self.crash = False
        self.gameDisplay = pygame.display.set_mode((screen_width, screen_height))

    def update(self, act):
        self.player.move(act)
        ## collision with obstacle
        for obstacle in self.obstacles:
            obstacle.update()
            self.obstacle_positions.pop(0)
            self.obstacle_positions.append((obstacle.get_position()))
            if self.player.get_position() == obstacle.get_position():
                self.crash = True
            elif self.player.get_position() in self.walls:
                self.crash = True

    def game_crashed(self):
        return self.crash

    # drawing game surface
    def draw_grid(self):
        for y in range(0, HEIGHT):
            for x in range(0, WIDTH):
                r = pygame.Rect((x * SIZE, y * SIZE), (SIZE, SIZE))
                if (x, y) in self.walls:
                   color = (255,255,255)
                elif (x, y) in self.obstacle_positions:
                    color = (0, 255, 0)
                elif (x, y) == self.player.get_position():
                    color = (255, 0, 0)
                elif (x, y) == self.goal.get_position():
                    color = (0, 0, 255)
                else:
                   color = (0,0,0)
                pygame.draw.rect(self.gameDisplay, color, r)
        if self.crash:
            draw_text("Game Over", pygame.font.SysFont('Bauhaus 93', 60), white, 500, 20, self.gameDisplay)

    def get_obstacles(self):
        return self.obstacle_positions
    
    def get_walls(self):
        return self.walls

    def get_player(self):
        return self.player.get_position()

    def get_goal(self):
        return self.goal.get_position()

    def get_score(self):
        return 100 - (self.goal.get_position()[0] - self.player.get_position()[0]) - (self.goal.get_position()[1] - self.player.get_position()[1])

def display(game):
    game.gameDisplay.fill((255, 255, 255))
    game.draw_grid()

def update_screen():
    pygame.display.update()

def initialize_game(game, agent, batch_size):
    state_init1 = agent.get_state(game, 60, 40)  
    action = [1, 0, 0, 0]
    game.update(action)
    state_init2 = agent.get_state(game, 60, 40)
    reward1 = agent.set_reward(game.get_goal(), game.get_player(), game.game_crashed())
    agent.remember(state_init1, action, reward1, state_init2, game.game_crashed())
    agent.replay_new(agent.memory, batch_size)

def run(params):
    pygame.init()
    walls = []

    agent = Agent(params)

    for x in range(WIDTH):
        walls.append((x, 0))
        walls.append((x, HEIGHT-1))

    for x in range(HEIGHT):
        walls.append((0, x))
        walls.append((WIDTH-1, x))

    #for x in range(HEIGHT-10):
    #    walls.append((18, x))

    #for x in range(10, HEIGHT):
    #    walls.append((42, x))

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

    game_count = 0

    while game_count < params['episodes']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        goal = Goal(50, 35)
        game = Game(walls, obstacles, goal)

        initialize_game(game, agent, params['batch_size'])

        while not game.game_crashed():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
            # agent.epsilon is set to give randomness to actions
            agent.epsilon = 1 - (game_count * params['epsilon_decay_linear'])

            # get old state
            state_old = agent.get_state(game, WIDTH, HEIGHT)

            # perform random actions based on agent.epsilon, or choose the action
            if random.uniform(0, 1) < agent.epsilon:
                final_move = to_categorical(random.randint(0, 3), num_classes=4)
            else:
                # predict action based on the old state
                prediction = agent.model.predict(state_old.reshape((1, 2400)))
                final_move = to_categorical(np.argmax(prediction[0]), num_classes=4)

            # perform new move and get new state
            game.update(final_move)
            state_new = agent.get_state(game, WIDTH, HEIGHT)

            # set reward for the new state
            reward = agent.set_reward(game.get_goal(), game.get_player(), game.game_crashed())

            # train short memory base on the new action and state
            agent.train_short_memory(state_old, final_move, reward, state_new, game.game_crashed())
            # store the new data into a long term memory
            agent.remember(state_old, final_move, reward, state_new, game.game_crashed())
            agent.replay_new(agent.memory, params['batch_size'])

            #display(game)
            #update_screen()
            pygame.time.wait(5)

        game_count += 1
        
        agent.model.save_weights(params['weights_path'])
        
        print(f'Game {game_count}      Score: {game.get_score()}')
        pygame.time.wait(500)
   

def main():
    params = define_parameters()
    
    params['bayesian_optimization'] = False    # Use bayesOpt.py for Bayesian Optimization
    run(params)

if __name__ == "__main__":
    main()
