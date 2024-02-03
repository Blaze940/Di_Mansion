import arcade
from game_configs import base_settings


class Environment:
    def __init__(self, str_map):
        global line
        row, col = 0, 0
        self.map = {}
        self.start = (13, 6)
        self.targets = None
        self.protection = None
        for line in str_map.strip().split('\n'):
            for char in line:
                self.map[row, col] = char
                if char == base_settings.MAP_START_AGENT:
                    self.start = (row, col)
                elif char == base_settings.MAP_TARGET:
                    self.targets = (row, col)
                col += 1
            col = 0
            row += 1

        self.height = row
        self.width = len(line)

    def do(self, state, action):
        move = base_settings.MOVES[action]
        new_state = (state[0] + move[0], state[1] + move[1])
        if self.is_not_allowed(new_state):
            reward = base_settings.REWARD_WALL
        else:
            state = new_state
            reward = base_settings.REWARD_LIFE_LOST = -100

        if action == "S":
            self.shoot()

        return state, reward

    def is_not_allowed(self, state):
        print("self.map[state] = ", self.map[state])
        return state not in self.map or self.map[state] == base_settings.MAP_WALL

    def shoot(self):
        return
