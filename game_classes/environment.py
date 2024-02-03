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

    def do(self, state, action, type_of_shoot):
        move = base_settings.MOVES[action]
        new_state = (state[0] + move[0], state[1] + move[1])
        if self.is_not_allowed(new_state):
            reward = base_settings.REWARD_WALL
        else:
            state = new_state
            reward = -100

        if action == "S":
            if type_of_shoot == "KILL":
                state = new_state
                reward = base_settings.REWARD_ENEMY_KILLED
            if type_of_shoot == "PROTECTION":
                state = new_state
                reward = base_settings.REWARD_PROTECTION_TOUCHED

        return state, reward

    def is_not_allowed(self, state):
        return state not in self.map or self.map[state] == base_settings.MAP_WALL

