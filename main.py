
from game_classes.environment import Environment
from game_configs import base_settings
from game_classes.game_window import GameWindow
from game_classes.agent import Agent
import matplotlib.pyplot as plt

if __name__ == '__main__':
    env = Environment(base_settings.MAP_LEVEL_BEGINNER)
    agent = Agent(env)
    agent.load(base_settings.AGENT_FILE)
    window = GameWindow(agent)
    window.setup()
    window.run()
    agent.save(base_settings.AGENT_FILE)
    plt.plot(agent.history)
    plt.show()
    print("hisstory = ",agent.history)