import arcade
import random
import matplotlib.pyplot as plt
import pickle
from os.path import exists

from game_classes.environment import Environment
from game_configs import base_settings
from game_classes.game_window import GameWindow
from game_classes.agent import Agent

if __name__ == '__main__':
    env = Environment(base_settings.MAP_LEVEL_BEGINNER)
    agent = Agent(env)
    window = GameWindow(agent)
    window.setup()
    window.run()