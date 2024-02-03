from game_configs import base_settings
from random import *


class Agent:

    def __init__(self, env, learning_rate=1, discount_factor=0.9):
        self.iteration = None
        self.score = None
        self.state = None
        self.env = env
        self.reset()
        self.qtable = {}
        for state in env.map:
            self.qtable[state] = {}
            for action in base_settings.ACTIONS:
                self.qtable[state][action] = 0.0

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.history = []
        self.noise = 0

    def reset(self):
        self.state = self.env.start
        self.score = 0
        self.iteration = 0

    def best_action(self):
        if random() < self.noise:
            return choice(base_settings.ACTIONS)
        else:
            return arg_max(self.qtable[self.state])

    def do(self, type_of_shoot):
        action = self.best_action()
        new_state, reward = self.env.do(self.state, action, type_of_shoot)
        self.score += reward
        self.iteration += 1
        # Q-learning
        self.qtable[self.state][action] += reward
        maxQ = max(self.qtable[new_state].values())
        delta = self.learning_rate * (reward + self.discount_factor * maxQ - self.qtable[self.state][action])
        self.qtable[self.state][action] += delta
        self.state = new_state

        if self.state == self.env.targets:
            self.history.append(self.score)
            self.noise *= 1 - 1E-1
        print("ACTION", action)
        return action

def arg_max(table):
    return max(table, key=table.get)
