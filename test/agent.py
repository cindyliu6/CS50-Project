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
        def __init__(self, params):
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
            model.add(Dense(4, activation='softmax'))
            opt = Adam(self.learning_rate)
            model.compile(loss='mse', optimizer=opt)

            return model
        
        def get_state(self, game, WIDTH, HEIGHT):
            state = []
            walls = game.get_walls()
            obstacles = game.get_obstacles()
            player = game.get_player()
            goal = game.get_goal()

            for i in range(WIDTH):
                for j in range(HEIGHT):
                    val = 0
                    if (i, j) == player:
                        val = 1
                    elif (i, j) == goal:
                        val = 2
                    elif (i, j) in walls:
                        val = 3
                    elif (i, j) in obstacles:
                        val = 4

                    state.append(val/4)
            
            return np.asarray(state)
        
        def set_reward(self, player, goal, dead):
            self.reward = 100 - (goal[0] - player[0]) + (goal[1] - player[1])
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
