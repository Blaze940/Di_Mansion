# GAME
GAME_NAME = 'DiMansion'
GAME_WINDOW_WIDTH = 15
GAME_WINDOW_HEIGHT = 14

# REWARD
REWARD_WALL = -300
REWARD_MOVE_AROUND = -100
REWARD_PROTECTION_TOUCHED = -1500
REWARD_SHOOT = 0
REWARD_LIFE_LOST = -1500
REWARD_STAGE_LOST = -1000
REWARD_DEFAULT = -10
REWARD_ENEMIES_GO_DOWN = -2500

REWARD_ENEMY_KILLED = 5000
REWARD_STAGE_CLEAR = 1000

# MAP
MAP_DIMENSION = [11, 12]
MAP_START_AGENT = '.'
MAP_ENEMY = '-'
MAP_PROTECTION = '@'
MAP_WALL = '#'
MAP_ENEMY_MISSILE = '!'
MAP_AGENT_MISSILE = '|'
MAP_TARGET = MAP_ENEMY

# AGENT
ACTION_LEFT, ACTION_RIGHT, ACTION_SHOOT = 'L', 'R', 'S'
ACTIONS = [ACTION_LEFT, ACTION_RIGHT, ACTION_SHOOT]

MOVES = {ACTION_LEFT: (0, -1),
         ACTION_RIGHT: (0, 1),
         ACTION_SHOOT: (0, 0)
         }

# SPRITE
SPRITE_SCALE = 0.4
SPRITE_SIZE = int(SPRITE_SCALE * 128)

# MAP LEVELS
MAP_LEVEL_BEGINNER = """
###############    
#   -------   #
#   -------   #
#   -------   #
#   -------   #
#   -------   #
#             #
#             #
#             #
#  @ @ @ @ @  #
#             #
#             #
#      .      #
###############     
"""

AGENT_FILE = 'agent.qtable'
