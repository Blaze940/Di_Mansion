import arcade
from game_configs import base_settings

class GameMap:
    def __init__(self,str_map):
        row, col = 0, 0
        self.map = {}
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