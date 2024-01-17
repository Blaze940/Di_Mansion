import arcade
import agent
from os.path import exists
from game_configs import base_settings

class GameWindow(arcade.Window):
    def __init__(self, agent):
        super().__init__(base_settings.GAME_WINDOW_WIDTH, base_settings.GAME_WINDOW_HEIGHT, base_settings.GAME_WINDOW_TITLE)