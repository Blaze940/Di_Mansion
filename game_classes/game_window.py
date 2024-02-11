import arcade
from game_configs import base_settings
import random

BULLET_SPEED = 5
ENEMY_SPEED = 2

MAX_PLAYER_BULLETS = 5

# This margin controls how close the enemy gets to the left or right side
# before reversing direction.
ENEMY_VERTICAL_MARGIN = 15
RIGHT_ENEMY_BORDER = (base_settings.GAME_WINDOW_WIDTH - 1) * base_settings.SPRITE_SIZE
LEFT_ENEMY_BORDER = base_settings.SPRITE_SIZE
SPRITE_SCALING_LASER = 0.8
# How many pixels to move the enemy down when reversing
ENEMY_MOVE_DOWN_AMOUNT = 30

# Game state
GAME_OVER = 1
PLAY_GAME = 0


class GameWindow(arcade.Window):
    def __init__(self, agent):
        super().__init__(base_settings.GAME_WINDOW_WIDTH * base_settings.SPRITE_SIZE,
                         base_settings.GAME_WINDOW_HEIGHT * base_settings.SPRITE_SIZE, base_settings.GAME_NAME)
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
        self.player = arcade.Sprite(":resources:images/enemies/bee.png", base_settings.SPRITE_SCALE)
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
        self.player = arcade.Sprite(":resources:images/enemies/bee.png", base_settings.SPRITE_SCALE)
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
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)

        # if self.game_state == GAME_OVER:
        # arcade.draw_text("GAME OVER", 250, 300, arcade.color.WHITE, 55)

    def update_enemies(self):
        # Move the enemy vertically
        for enemy in self.enemies:
            enemy.center_x += self.enemy_change_x

        # Check every enemy to see if any hit the edge. If so, reverse the
        # direction and flag to move down.
        move_down = False
        for enemy in self.enemies:
            if enemy.right > RIGHT_ENEMY_BORDER and self.enemy_change_x > 0:
                self.enemy_change_x *= -1
                move_down = True
                self.EVENT = "ENEMIES_MOVE_DOWN"
            if enemy.left < LEFT_ENEMY_BORDER and self.enemy_change_x < 0:
                self.enemy_change_x *= -1
                move_down = True
                self.EVENT = "ENEMIES_MOVE_DOWN"

        # Did we hit the edge above, and need to move t he enemy down?
        if move_down:
            # Yes
            for enemy in self.enemies:
                # Move enemy down
                enemy.center_y -= ENEMY_MOVE_DOWN_AMOUNT

    def allow_enemies_to_fire(self):
        """
        See if any enemies will fire this frame.
        """
        # Track which x values have had a chance to fire a bullet.
        # Since enemy list is build from the bottom up, we can use
        # this to only allow the bottom row to fire.
        x_spawn = []
        for enemy in self.enemies:
            # Adjust the chance depending on the number of enemies. Fewer
            # enemies, more likely to fire.
            chance = 4 + len(self.enemies) * 4

            # Fire if we roll a zero, and no one else in this column has had
            # a chance to fire.
            if random.randrange(chance) == 0 and enemy.center_x not in x_spawn:
                # Create a bullet
                bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", base_settings.SPRITE_SCALE)

                # Angle down.
                bullet.angle = 180

                # Give the bullet a speed
                bullet.change_y = -BULLET_SPEED

                # Position the bullet so its top id right below the enemy
                bullet.center_x = enemy.center_x
                bullet.top = enemy.bottom

                # Add the bullet to the appropriate list
                self.enemies_bullets.append(bullet)

            # Ok, this column has had a chance to fire. Add to list so we don't
            # try it again this frame.
            x_spawn.append(enemy.center_x)

    def process_enemy_bullets(self):

        # Move the bullets
        self.enemies_bullets.update()

        # Loop through each bullet
        for bullet in self.enemies_bullets:
            # Check this bullet to see if it hit a shield
            hit_list = arcade.check_for_collision_with_list(bullet, self.protections)

            # If it did, get rid of the bullet and shield blocks
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                continue

            # See if the player got hit with a bullet
            if arcade.check_for_collision_with_list(self.player, self.enemies_bullets):
                self.game_state = GAME_OVER
                self.EVENT = "DIED"
            # If the bullet falls off the screen get rid of it
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()
                # self.enemies_bullets.remove(bullet)

    def player_shoot(self):
        if len(self.player_bullets) < MAX_PLAYER_BULLETS:
            # Create a bullet
            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", base_settings.SPRITE_SCALE)

            # The image points to the right, and we want it to point up. So
            # rotate it.
            bullet.angle = 90

            # Give the bullet a speed
            bullet.change_y = BULLET_SPEED

            # Position the bullet
            bullet.center_x = self.player.center_x
            bullet.bottom = self.player.top

            # Add the bullet to the appropriate lists
            self.player_bullets.append(bullet)

    def process_player_bullets(self):

        # Move the bullets
        self.player_bullets.update()

        # Loop through each bullet
        for bullet in self.player_bullets:

            # Check this bullet to see if it hit a enemy
            hit_list = arcade.check_for_collision_with_list(bullet, self.protections)
            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                    self.EVENT = "SHOOT_PROTECTION"
                continue

            # Check this bullet to see if it hit a enemy
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                self.EVENT = "KILL_ENEMY"

            # For every enemy we hit, add to the score and remove the enemy
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > base_settings.GAME_WINDOW_WIDTH * base_settings.SPRITE_SIZE:
                bullet.remove_from_sprite_lists()

    def on_update(self, delta_time):
        """ Movement and game logic """
        enemies_bullets = [
            (int(sprite.center_x / base_settings.SPRITE_SIZE), int(sprite.center_y / base_settings.SPRITE_SIZE)) for
            sprite in self.enemies_bullets]
        enemies = [
            (int(sprite.center_x / base_settings.SPRITE_SIZE), int(sprite.center_y / base_settings.SPRITE_SIZE)) for
            sprite in self.enemies]
        print(enemies_bullets)
        self.EVENT = ""
        action = self.agent.do("", enemies_bullets, enemies, self.level_finished)
        if self.EVENT in ["DIED", "ENEMIES_MOVE_DOWN"]:
            self.agent.do(self.EVENT, enemies_bullets, enemies, self.level_finished)

        if action == "S":
            self.player_shoot()
            self.agent.do(self.EVENT, enemies_bullets, enemies, self.level_finished)

        if len(self.enemies) == 0:
            self.level_finished = True
            #self.setup_level_one()


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
