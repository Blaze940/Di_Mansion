import arcade
from game_configs import base_settings

class GameWindow(arcade.Window):
    def __init__(self, agent):
        super().__init__(base_settings.GAME_WINDOW_WIDTH * base_settings.SPRITE_SIZE, base_settings.GAME_WINDOW_HEIGHT * base_settings.SPRITE_SIZE, base_settings.GAME_NAME)
        self.enemies = None
        self.protections = None
        self.walls = None
        self.player = None
        self.env = agent.env
        self.agent = agent
    def state_to_xy(self, state):
        return (state[1] + 0.5) * base_settings.SPRITE_SIZE, \
               (self.env.height - state[0] - 0.5) * base_settings.SPRITE_SIZE

    def setup(self):
        self.walls = arcade.SpriteList()
        self.protections = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.player = arcade.Sprite(":resources:images/enemies/bee.png", base_settings.SPRITE_SCALE)

        for row in range(self.env.height):
            for col in range(self.env.width):
                if self.env.map[row, col] == base_settings.MAP_WALL:
                    sprite = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", base_settings.SPRITE_SCALE)
                    sprite.center_x, sprite.center_y = self.state_to_xy((row, col))
                    self.walls.append(sprite)
                elif self.env.map[row, col] == base_settings.MAP_PROTECTION:
                    sprite = arcade.Sprite(":resources:images/tiles/boxCrate_single.png", base_settings.SPRITE_SCALE)
                    sprite.center_x, sprite.center_y = self.state_to_xy((row, col))
                    self.protections.append(sprite)
                elif self.env.map[row, col] == base_settings.MAP_ENEMY:
                    sprite = arcade.Sprite(":resources:images/enemies/slimeBlock.png", base_settings.SPRITE_SCALE)
                    sprite.center_x, sprite.center_y = self.state_to_xy((row, col))
                    self.enemies.append(sprite)

        self.update_player()

    def on_draw(self):
        arcade.start_render()
        self.walls.draw()
        self.protections.draw()
        self.enemies.draw()
        self.player.draw()


    def update_player(self):
        self.player.center_x, self.player.center_y = self.state_to_xy(self.agent.state)
