import os
import pygame
import argparse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from random import randint
from keras.utils import to_categorical
import random
import statistics
import game_test as game
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import pandas as pd
from operator import add
import collections

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
    params['weights_path'] = 'weights/weights3.hdf5'
    params['load_weights'] = True
    params['train'] = False
    params['plot_score'] = True
    return params

class Agent(object):
        def __init__(self, params, x, y, goal_x, goal_y):
            self.player = game.Player(x, y)
            self.goal = goal
            self.reward = 0
            self.gamma = 0.9
            self.dataframe = pd.DataFrame()
            self.short_memory = np.array([])
            self.agent_target = 1
            self.agent_predict = 0
            self.learning_rate = params['learning_rate']        
            self.epsilon = 1
            self.actual = []
            self.first_layer = params['first_layer_size']
            self.second_layer = params['second_layer_size']
            self.third_layer = params['third_layer_size']
            self.memory = collections.deque(maxlen=params['memory_size'])
            self.weights = params['weights_path']
            self.load_weights = params['load_weights']
            self.model = self.network()

        def network(self):
            model = Sequential()
            model.add(Dense(self.first_layer, activation='relu', input_dim=2400))
            model.add(Dense(self.second_layer, activation='relu'))
            model.add(Dense(self.third_layer, activation='relu'))
            model.add(Dense(3, activation='softmax'))
            opt = Adam(self.learning_rate)
            model.compile(loss='mse', optimizer=opt)

            return model
        
        def get_state(self, walls, obstacles, goal):
            state = []

            for i in range(len(60)):
                for j in range(len(40)):
                    val = 0
                    if i == self.player.get_position[0] and j == self.player.get_position[1]:
                        val = 1
                    elif i == goal.get_position[0] and j == goal.get_position[1]:
                        val = 2
                    elif (i, j) in walls:
                        val = 3
                    elif (i, j) in obstacles:
                        val = 4

                    state.append(val/4)

            
            return np.asarray(state)
        
        def set_reward(self, dead):
            self.reward = 100 - (self.goal.get_position[0] - self.player.get_position[0]) - (self.goal.get_position[1] - self.player.get_position[1])
            if dead:
                self.reward = -200
                return self.reward
            return self.reward

        def remember(self, state, action, reward, next_state, done):
            self.memory.append((state, action, reward, next_state, done))

        def replay_new(self, memory, batch_size):
            if len(memory) > batch_size:
                minibatch = random.sample(memory, batch_size)
            else:
                minibatch = memory
            for state, action, reward, next_state, done in minibatch:
                target = reward
                if not done:
                    target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
                target_f = self.model.predict(np.array([state]))
                target_f[0][np.argmax(action)] = target
                self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

        def train_short_memory(self, state, action, reward, next_state, done):
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 2400)))[0])
            target_f = self.model.predict(state.reshape((1, 2400)))
            target_f[0][np.argmax(action)] = target
            self.model.fit(state.reshape((1, 2400)), target_f, epochs=1, verbose=0)


class Game():
    def __init__(self, walls, obstacles):
        self.player = Player(5, 5)
        self.walls = walls
        self.obstacles = obstacles
        self.crash = False
        self.gameDisplay = pygame.display.set_mode((900, 600))

def run(display_option, speed, params):
    pygame.init()
    agent = Agent(params)
    weights_filepath = params['weights_path']
    if params['load_weights']:
        agent.model.load_weights(weights_filepath)
        print("weights loaded")
    counter_games = 0
    score_plot = []
    counter_plot = []
    record = 0
    total_score = 0
    while counter_games < params['episodes']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Initialize classes
        game = Game(440, 440)
        player1 = game.player
        food1 = game.food

        # Perform first move
        initialize_game(player1, game, food1, agent, params['batch_size'])
        if display_option:
            display(player1, food1, game, record)

        while not game.crash:
            if not params['train']:
                agent.epsilon = 0.00
            else:
                # agent.epsilon is set to give randomness to actions
                agent.epsilon = 1 - (counter_games * params['epsilon_decay_linear'])

            # get old state
            state_old = agent.get_state(game, player1, food1)

            # perform random actions based on agent.epsilon, or choose the action
            if random.uniform(0, 1) < agent.epsilon:
                final_move = to_categorical(randint(0, 2), num_classes=3)
            else:
                # predict action based on the old state
                prediction = agent.model.predict(state_old.reshape((1, 11)))
                final_move = to_categorical(np.argmax(prediction[0]), num_classes=3)

            # perform new move and get new state
            player1.do_move(final_move, player1.x, player1.y, game, food1, agent)
            state_new = agent.get_state(game, player1, food1)

            # set reward for the new state
            reward = agent.set_reward(player1, game.crash)

            if params['train']:
                # train short memory base on the new action and state
                agent.train_short_memory(state_old, final_move, reward, state_new, game.crash)
                # store the new data into a long term memory
                agent.remember(state_old, final_move, reward, state_new, game.crash)

            record = get_record(game.score, record)
            if display_option:
                display(player1, food1, game, record)
                pygame.time.wait(speed)
        if params['train']:
            agent.replay_new(agent.memory, params['batch_size'])
        counter_games += 1
        total_score += game.score
        print(f'Game {counter_games}      Score: {game.score}')
        score_plot.append(game.score)
        counter_plot.append(counter_games)
    mean, stdev = get_mean_stdev(score_plot)
    if params['train']:
        agent.model.save_weights(params['weights_path'])
        total_score, mean, stdev = test(display_option, speed, params)
    if params['plot_score']:
        plot_seaborn(counter_plot, score_plot, params['train'])
    print('Total score: {}   Mean: {}   Std dev:   {}'.format(total_score, mean, stdev))
    return total_score, mean, stdev



if __name__ == '__main__':
    # Set options to activate or deactivate the game view, and its speed
    pygame.font.init()
    #parser = argparse.ArgumentParser()
    params = define_parameters()
    #parser.add_argument("--display", type=bool, default=False)
    #parser.add_argument("--speed", type=int, default=50)
    #args = parser.parse_args()
    params['bayesian_optimization'] = False    # Use bayesOpt.py for Bayesian Optimization
    run(True, 50, params)