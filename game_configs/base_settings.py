
# GAME
GAME_NAME = 'DiMansion'
GAME_WINDOW_WIDTH = 15
GAME_WINDOW_HEIGHT = 14


# REWARD
REWARD_WALL = -286
REWARD_PROTECTION_TOUCHED = -100
REWARD_LIFE_LOST = -100
REWARD_STAGE_LOST = -1000
REWARD_DEFAULT = -1

REWARD_ENEMY_KILLED = 200
REWARD_STAGE_CLEAR = 1000

# MAP
MAP_DIMENSION = [11,12]
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
#             #
#  @ @ @ @ @  #
#             #
#      .      #
###############     
"""