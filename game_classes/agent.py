from game_configs import base_settings


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
