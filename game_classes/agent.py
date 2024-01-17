from game_configs import base_settings

class Agent :

    def __init__(self, env, learning_rate = 1, discount_factor = 0.9):
        self.score = 0