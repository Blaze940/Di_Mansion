from game_configs import base_settings
from random import *
import pickle
from os.path import exists


class Agent:

    def __init__(self, env, learning_rate=1, discount_factor=0.9):
        self.env = env
        self.reset()
        self.qtable = {}
        self.add_state(self.state)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.history = []
        self.noise = 0

    def reset(self):
        self.position = self.env.start
        self.score = 0
        self.iteration = 0
        self.state = self.env.get_radar(self.position, [], [])

    def best_action(self):
        if random() < self.noise:
            return choice(base_settings.ACTIONS)
        else:
            return arg_max(self.qtable[self.state])

    def do(self, type_of_shoot, bullets, enemies):
        action = self.best_action()
        new_state, position, reward = self.env.do(self.position, action, type_of_shoot, bullets, enemies)
        self.score += reward
        self.iteration += 1
        self.position = position

        # Q-learning
        self.add_state(new_state)
        maxQ = max(self.qtable[new_state].values())
        delta = self.learning_rate * (reward + self.discount_factor * maxQ - self.qtable[self.state][action])
        self.qtable[self.state][action] += delta
        self.state = new_state

        if type_of_shoot == "KILL_ENEMY":
            self.history.append(self.score)
            self.noise *= 1 - 1E-1
        print("ACTION", action)
        return action

    def load(self, filename):
        if exists(filename):
            with open(filename, 'rb') as file:
                self.qtable = pickle.load(file)
            self.reset()

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.qtable, file)

    def add_state(self, state):
        if state not in self.qtable:
            self.qtable[state] = {}
            for action in base_settings.ACTIONS:
                self.qtable[state][action] = 0.0


def arg_max(table):
    return max(table, key=table.get)
