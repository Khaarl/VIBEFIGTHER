import arcade
import os

# Screen Constants
SCREEN_TITLE = "Arcade Fighter"

# Resolution Options
RESOLUTIONS = {
    "SD": (800, 600),
    "HD": (1280, 720),
    "FHD": (1920, 1080)
}

# Current resolution tracking
_CURRENT_RESOLUTION = "HD"  # Default to HD
SCREEN_WIDTH, SCREEN_HEIGHT = RESOLUTIONS[_CURRENT_RESOLUTION]

def set_resolution(res_key: str):
    """Set the current resolution and update constants"""
    global SCREEN_WIDTH, SCREEN_HEIGHT, _CURRENT_RESOLUTION
    if res_key in RESOLUTIONS:
        _CURRENT_RESOLUTION = res_key
        SCREEN_WIDTH, SCREEN_HEIGHT = RESOLUTIONS[res_key]
        # Update dependent constants
        HEALTHBAR_PLAYER2_X = SCREEN_WIDTH - 50 - HEALTHBAR_WIDTH

# Menu States
MENU_MAIN = "main"
MENU_OPTIONS = "options"
MENU_VIDEO = "video"
MENU_AUDIO = "audio"
MENU_MUSIC = "music"

# Audio Constants
DEFAULT_VOLUME = 0.5
MUSIC_FILES = [
    "arcade_fighter/assets/MUSIC/09 - DavidKBD - Purgatory Pack - MiniLoop 01.ogg",
    "arcade_fighter/assets/MUSIC/12 - DavidKBD - Purgatory Pack - MiniLoop 04.ogg",
    "arcade_fighter/assets/MUSIC/13 - DavidKBD - Purgatory Pack - MiniLoop 05.ogg",
    "arcade_fighter/assets/MUSIC/17 - DavidKBD - Purgatory Pack - MiniLoop 09.ogg",
    "arcade_fighter/assets/MUSIC/21 - DavidKBD - Purgatory Pack - MiniLoop 13.ogg",
    "arcade_fighter/assets/MUSIC/22 - DavidKBD - Purgatory Pack - MiniLoop 14.ogg"
]

BACKGROUND_IMAGES = [
    "arcade_fighter/assets/images/STATIC/khaaaarl_giant_bat_spread_wings_screaming_sonic_wawwes_by_jun_b5f9261a-da76-43a2-b967-78bbf0a0dd63_1.png",
    "arcade_fighter/assets/images/STATIC/khaaaarl_giant_bat_spread_wings_screaming_sonic_wawwes_by_jun_33df75ef-efbc-4a90-8a6f-8a656c8f9431_3.png"
]

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

# UI Colors
BLOOD_RED = (136, 8, 8)
OBSIDIAN = (10, 10, 10)
ASH_GRAY = (30, 30, 30)
BONE_WHITE = (220, 220, 210)
RUST = (180, 65, 21)

# UI Elements
BUTTON_BORDER = 3
FLICKER_INTERVAL = 2.0  # seconds
OCCULT_SYMBOL_SCALE = 0.15

# Font Settings
FONT_PRIMARY = ":resources:fonts/Blackmetal.ttf"
FONT_SIZE_TITLE = 72
FONT_SIZE_BUTTON = 28
FONT_SIZE_SMALL = 18

# Colors
WHITE = arcade.color.WHITE
BLACK = arcade.color.BLACK

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
KEY_JUMP_P1 = arcade.key.SPACE
KEY_ATTACK_P1 = arcade.key.F

# Player 2
KEY_UP_P2 = arcade.key.UP
KEY_DOWN_P2 = arcade.key.DOWN
KEY_LEFT_P2 = arcade.key.LEFT
KEY_RIGHT_P2 = arcade.key.RIGHT
KEY_JUMP_P2 = arcade.key.ENTER
KEY_ATTACK_P2 = arcade.key.RCTRL

# Debug Settings
# Debug settings - default to False in production
DEBUG_MODE = os.getenv('ARCADE_DEBUG', 'False').lower() in ('true', '1', 't')
DEBUG_SHOW_HITBOXES = DEBUG_MODE
DEBUG_SHOW_VECTORS = DEBUG_MODE
DEBUG_SHOW_ANIM_STATES = DEBUG_MODE

# Debug Controls
KEY_TOGGLE_DEBUG = arcade.key.F1
KEY_RELOAD_ASSETS = arcade.key.F5
KEY_TOGGLE_HITBOXES = arcade.key.F2
KEY_TOGGLE_VECTORS = arcade.key.F3
KEY_TOGGLE_ANIM_DEBUG = arcade.key.F4