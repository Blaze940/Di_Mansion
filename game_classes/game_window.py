import arcade
from game_configs import base_settings
import random

BULLET_SPEED = 23
ENEMY_SPEED = 23

MAX_PLAYER_BULLETS = 2

ENEMY_VERTICAL_MARGIN = 15
RIGHT_ENEMY_BORDER = (base_settings.GAME_WINDOW_WIDTH - 1) * base_settings.SPRITE_SIZE
LEFT_ENEMY_BORDER = base_settings.SPRITE_SIZE
SPRITE_SCALING_LASER = 0.8
ENEMY_MOVE_DOWN_AMOUNT = 30

# Game state
GAME_OVER = 1
PLAY_GAME = 0


class GameWindow(arcade.Window):
    def __init__(self, agent):
        super().__init__(base_settings.GAME_WINDOW_WIDTH * base_settings.SPRITE_SIZE,
                         base_settings.GAME_WINDOW_HEIGHT * base_settings.SPRITE_SIZE, base_settings.GAME_NAME)
        self.enemies_bullets_coords = None
        self.enemies_coords = None
        self.enemies = None
        self.enemies_bullets = None
        self.protections = None
        self.walls = None
        self.player = None
        self.player_bullets = None
        self.env = agent.env
        self.agent = agent
        self.game_state = PLAY_GAME
        self.score = 0
        self.enemy_change_x = -ENEMY_SPEED
        self.EVENT = ""
        self.level_finished = False

    def state_to_xy(self, state):
        return (state[1] + 0.5) * base_settings.SPRITE_SIZE, \
               (self.env.height - state[0] - 0.5) * base_settings.SPRITE_SIZE

    def setup(self):
        self.walls = arcade.SpriteList()
        self.protections = arcade.SpriteList()
        self.player = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", base_settings.SPRITE_SCALE)
        self.game_state = PLAY_GAME
        self.player_bullets = arcade.SpriteList()
        self.score = 0
        for state in self.env.map:
            if self.env.map[state] == base_settings.MAP_WALL:
                sprite = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", base_settings.SPRITE_SCALE)
                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.walls.append(sprite)
            elif self.env.map[state] == base_settings.MAP_PROTECTION:
                self.build_protection(self.state_to_xy(state))

        self.setup_level_one()

        self.update_player()

    def setup_level_one(self):
        self.walls = arcade.SpriteList()
        self.protections = arcade.SpriteList()
        self.player = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", base_settings.SPRITE_SCALE)
        self.game_state = PLAY_GAME
        self.player_bullets = arcade.SpriteList()
        self.score = 0
        self.enemies = arcade.SpriteList()
        self.enemies_bullets = arcade.SpriteList()
        for state in self.env.map:
            if self.env.map[state] == base_settings.MAP_WALL:
                sprite = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", base_settings.SPRITE_SCALE)
                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.walls.append(sprite)
            elif self.env.map[state] == base_settings.MAP_PROTECTION:
                self.build_protection(self.state_to_xy(state))
            elif self.env.map[state] == base_settings.MAP_ENEMY:
                sprite = arcade.Sprite(":resources:images/enemies/slimeBlock.png", base_settings.SPRITE_SCALE)
                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.enemies.append(sprite)

    def build_protection(self, state):
        x_start, y_start = int(state[0]), int(state[1])
        shield_block_width = 10
        shield_block_height = 10
        shield_width_count = 5
        shield_height_count = 5
        for x in range(x_start,
                       x_start + shield_width_count * shield_block_width,
                       shield_block_width):
            for y in range(y_start,
                           y_start + shield_height_count * shield_block_height,
                           shield_block_height):
                shield_sprite = arcade.SpriteSolidColor(shield_block_width,
                                                        shield_block_height,
                                                        arcade.color.WHITE)
                shield_sprite.center_x = x
                shield_sprite.center_y = y
                self.protections.append(shield_sprite)

    def on_draw(self):
        self.clear()
        arcade.start_render()
        self.walls.draw()
        self.protections.draw()
        self.enemies.draw()
        self.player.draw()
        self.enemies_bullets.draw()
        self.player_bullets.draw()
        arcade.draw_text(f"Score: {self.agent.score}", 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text(f"Noise: {self.agent.noise}", 200, 20, arcade.color.WHITE, 14)
        arcade.draw_text(f"Event: {self.EVENT}", 400, 20, arcade.color.WHITE, 14)
    def update_enemies(self):
        for enemy in self.enemies:
            enemy.center_x += self.enemy_change_x

        move_down = False
        for enemy in self.enemies:
            if enemy.right > RIGHT_ENEMY_BORDER and self.enemy_change_x > 0:
                self.enemy_change_x *= -1
                move_down = True
                self.agent.do("ENEMIES_MOVE_DOWN", self.enemies_bullets_coords, self.enemies_coords, self.level_finished)
                self.EVENT = "ENEMIES_MOVE_DOWN"
            if enemy.left < LEFT_ENEMY_BORDER and self.enemy_change_x < 0:
                self.enemy_change_x *= -1
                move_down = True
                self.agent.do("ENEMIES_MOVE_DOWN", self.enemies_bullets_coords, self.enemies_coords,
                              self.level_finished)
                self.EVENT = "ENEMIES_MOVE_DOWN"
            if enemy.bottom <= base_settings.SPRITE_SIZE:
                self.agent.do("ENEMIES_GOT_DOWN", self.enemies_bullets_coords, self.enemies_coords,
                              self.level_finished)
                self.EVENT = "ENEMIES_GOT_DOWN"
                self.game_state = GAME_OVER
                self.agent.history.append(self.agent.score)
                self.agent.reset()
                self.setup_level_one()
                break

        if move_down:
            for enemy in self.enemies:
                enemy.center_y -= ENEMY_MOVE_DOWN_AMOUNT

    def allow_enemies_to_fire(self):
        x_spawn = []
        for enemy in self.enemies:
            chance = 150

            if random.randrange(chance) == 0 and enemy.center_x not in x_spawn:
                bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", base_settings.SPRITE_SCALE)
                bullet.angle = 180
                bullet.change_y = -BULLET_SPEED
                bullet.center_x = enemy.center_x
                bullet.top = enemy.bottom
                self.enemies_bullets.append(bullet)
            x_spawn.append(enemy.center_x)

    def process_enemy_bullets(self):

        self.enemies_bullets.update()
        for bullet in self.enemies_bullets:
            hit_list = arcade.check_for_collision_with_list(bullet, self.protections)

            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                continue

            if arcade.check_for_collision_with_list(self.player, self.enemies_bullets):
                self.agent.do("DIED", self.enemies_bullets_coords, self.enemies_coords, self.level_finished)
                self.game_state = GAME_OVER
                self.EVENT = "DIED"
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def player_shoot(self):

        if len(self.player_bullets) < MAX_PLAYER_BULLETS:
            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", base_settings.SPRITE_SCALE)
            bullet.angle = 90
            bullet.change_y = BULLET_SPEED
            bullet.center_x = self.player.center_x
            bullet.bottom = self.player.top
            self.player_bullets.append(bullet)

    def process_player_bullets(self):

        self.player_bullets.update()
        for bullet in self.player_bullets:
            hit_list = arcade.check_for_collision_with_list(bullet, self.protections)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                    self.agent.do("SHOOT_PROTECTION", self.enemies_bullets_coords, self.enemies_coords, self.level_finished)
                    self.EVENT = "SHOOT_PROTECTION"
                continue

            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies)

            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                self.agent.do("KILL_ENEMY", self.enemies_bullets_coords, self.enemies_coords, self.level_finished)
                self.EVENT = "KILL_ENEMY"

            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1

            if bullet.bottom > base_settings.GAME_WINDOW_WIDTH * base_settings.SPRITE_SIZE:
                bullet.remove_from_sprite_lists()

    def on_update(self, delta_time):
        if self.game_state == GAME_OVER:
            self.agent.history.append(self.agent.score)
            self.agent.reset()
            self.setup_level_one()

        self.enemies_bullets_coords = [
            (int(sprite.center_x / base_settings.SPRITE_SIZE), int(sprite.center_y / base_settings.SPRITE_SIZE)) for
            sprite in self.enemies_bullets]
        self.enemies_coords = [
            (int(sprite.center_x / base_settings.SPRITE_SIZE), int(sprite.center_y / base_settings.SPRITE_SIZE)) for
            sprite in self.enemies]

        action = self.agent.do("", self.enemies_bullets_coords, self.enemies_coords, self.level_finished)
        if action == "S":
            self.player_shoot()

        if len(self.enemies) == 0:
            self.level_finished = True
            self.agent.history.append(self.agent.score)
            self.agent.reset()
            self.setup_level_one()



        self.update_enemies()
        self.allow_enemies_to_fire()
        self.process_enemy_bullets()
        self.process_player_bullets()
        self.update_player()

    def update_player(self):
        self.player.center_x, self.player.center_y = self.state_to_xy(self.agent.position)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.agent.reset()
            self.setup_level_one()
        elif key == arcade.key.X:
            self.agent.noise = 1
            self.agent.reset()
        self.update_player()
