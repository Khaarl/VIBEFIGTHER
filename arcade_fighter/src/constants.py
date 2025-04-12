import arcade

# Screen Constants
SCREEN_TITLE = "Arcade Fighter"

# Resolution Options
RESOLUTIONS = {
    "SD": (800, 600),
    "HD": (1280, 720), 
    "FHD": (1920, 1080)
}

# Default resolution
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

# Menu States
MENU_MAIN = "main"
MENU_OPTIONS = "options"
MENU_VIDEO = "video"
MENU_AUDIO = "audio"
MENU_MUSIC = "music"

# Fullscreen state
FULLSCREEN = False

# UI Constants
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20
HEALTHBAR_WIDTH = 200
HEALTHBAR_HEIGHT = 20
HEALTHBAR_OFFSET_Y = 30
HEALTHBAR_PLAYER1_X = 50
HEALTHBAR_PLAYER2_X = SCREEN_WIDTH - 50 - HEALTHBAR_WIDTH
UI_FONT_SIZE = 18

# Colors
WHITE = arcade.color.WHITE
BLACK = arcade.color.BLACK
BLUE = arcade.color.BLUE
LIGHT_BLUE = arcade.color.LIGHT_BLUE
DARK_BLUE = arcade.color.DARK_BLUE_GRAY
GOLD = arcade.color.GOLD
RED = arcade.color.RED
GREEN = arcade.color.GREEN
HEALTH_COLOR = arcade.color.GREEN
HEALTH_BACKGROUND_COLOR = arcade.color.DARK_RED

# Physics Constants
GRAVITY = 1.0
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20

# Character Constants
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
PLAYER_START_HP = 100

# Game States
STATE_IDLE = "idle"
STATE_WALKING = "walking"
STATE_JUMPING = "jumping"
STATE_ATTACKING = "attacking"
STATE_HIT = "hit"
STATE_DEAD = "dead"

# Character Directions
RIGHT_FACING = 0
LEFT_FACING = 1

# Game Flow
ROUNDS_TO_WIN = 2

# Input Keys
# Player 1
KEY_UP_P1 = arcade.key.W
KEY_DOWN_P1 = arcade.key.S
KEY_LEFT_P1 = arcade.key.A
KEY_RIGHT_P1 = arcade.key.D
KEY_JUMP_P1 = arcade.key.W
KEY_ATTACK_P1 = arcade.key.SPACE

# Player 2
KEY_UP_P2 = arcade.key.UP
KEY_DOWN_P2 = arcade.key.DOWN
KEY_LEFT_P2 = arcade.key.LEFT
KEY_RIGHT_P2 = arcade.key.RIGHT
KEY_JUMP_P2 = arcade.key.UP
KEY_ATTACK_P2 = arcade.key.ENTER

# Debug Settings
DEBUG_MODE = False
DEBUG_SHOW_HITBOXES = True
DEBUG_SHOW_VECTORS = True
DEBUG_SHOW_ANIM_STATES = True

# Debug Controls
KEY_TOGGLE_DEBUG = arcade.key.F1
KEY_RELOAD_ASSETS = arcade.key.F5
KEY_TOGGLE_HITBOXES = arcade.key.F2
KEY_TOGGLE_VECTORS = arcade.key.F3
KEY_TOGGLE_ANIM_DEBUG = arcade.key.F4