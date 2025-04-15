# Character Directions
RIGHT_FACING = 0
LEFT_FACING = 1

# Character States
STATE_IDLE = "idle"
STATE_WALKING = "walking"
STATE_JUMPING = "jumping"
STATE_ATTACKING = "attacking"
STATE_HIT = "hit"
STATE_DEAD = "dead"


# UI Elements
OCCULT_SYMBOL_SCALE = 0.15


# UI Effects
FLICKER_INTERVAL = 2.0  # seconds


# Background Images
BACKGROUND_IMAGES = [
    "arcade_fighter/assets/images/STATIC/khaaaarl_giant_bat_spread_wings_screaming_sonic_wawwes_by_jun_b5f9261a-da76-43a2-b967-78bbf0a0dd63_1.png",
    "arcade_fighter/assets/images/STATIC/khaaaarl_giant_bat_spread_wings_screaming_sonic_wawwes_by_jun_33df75ef-efbc-4a90-8a6f-8a656c8f9431_3.png"
]


# Menu States
MENU_MAIN = "main"
MENU_OPTIONS = "options"
MENU_VIDEO = "video"
MENU_AUDIO = "audio"
MENU_MUSIC = "music"

"""Centralized configuration for Arcade Fighter game"""

import arcade
import os
from typing import Dict, Tuple

# ========================
# SCREEN/DISPLAY SETTINGS
# ========================
SCREEN_TITLE = "Arcade Fighter"

# Resolution options
RESOLUTIONS: Dict[str, Tuple[int, int]] = {
    "SD": (800, 600),
    "HD": (1280, 720), 
    "FHD": (1920, 1080)
}

# Current resolution tracking
_CURRENT_RESOLUTION = "HD"  # Default
SCREEN_WIDTH, SCREEN_HEIGHT = RESOLUTIONS[_CURRENT_RESOLUTION]
FULLSCREEN = False
BACKGROUND_COLOR = arcade.csscolor.CORNFLOWER_BLUE

# ========================
# INPUT/CONTROLS
# ========================
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

# Debug controls
KEY_TOGGLE_DEBUG = arcade.key.F1
KEY_RELOAD_ASSETS = arcade.key.F5
KEY_TOGGLE_HITBOXES = arcade.key.F2
KEY_TOGGLE_VECTORS = arcade.key.F3
KEY_TOGGLE_ANIM_DEBUG = arcade.key.F4

# ========================
# GAMEPLAY SETTINGS
# ========================
# Physics
GRAVITY = 1.0
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20

# Character
CHARACTER_SCALING = 1.0
CHARACTER_SCALING_BY_RESOLUTION = {
    "SD": 1.2,
    "HD": 1.0,
    "FHD": 0.8
}

# Combat
PLAYER_START_HP = 100
ATTACK_DAMAGE = 10
ATTACK_DURATION = 0.5
ATTACK_COOLDOWN = 1.0
ATTACK_HITBOX = {
    'width': 60,
    'height': 100,
    'offset_x': 40,
    'offset_y': 0
}

# Game flow
ROUNDS_TO_WIN = 2

# ========================
# UI/GRAPHICS SETTINGS
# ========================
# Health bars
HEALTHBAR_WIDTH = 200
HEALTHBAR_HEIGHT = 20
HEALTHBAR_OFFSET_Y = 30
HEALTHBAR_PLAYER1_X = 50
HEALTHBAR_PLAYER2_X = SCREEN_WIDTH - 50 - HEALTHBAR_WIDTH
HEALTHBAR_COLOR = arcade.color.RED
HEALTHBAR_BG_COLOR = arcade.color.DARK_GRAY

# Buttons
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20
BUTTON_BORDER = 3

# Colors
BLOOD_RED = (136, 8, 8)
OBSIDIAN = (10, 10, 10)
ASH_GRAY = (30, 30, 30)
BONE_WHITE = (220, 220, 210)
RUST = (180, 65, 21)
WHITE = arcade.color.WHITE
BLACK = arcade.color.BLACK

# Fonts
FONT_PRIMARY = ":resources:fonts/Blackmetal.ttf"
FONT_SIZE_TITLE = 72
FONT_SIZE_BUTTON = 28
FONT_SIZE_SMALL = 18
UI_FONT_SIZE = 18

# ========================
# AUDIO SETTINGS
# ========================
DEFAULT_VOLUME = 0.5
MUSIC_FILES = [
    "assets/MUSIC/09 - DavidKBD - Purgatory Pack - MiniLoop 01.ogg",
    "assets/MUSIC/12 - DavidKBD - Purgatory Pack - MiniLoop 04.ogg",
    "assets/MUSIC/13 - DavidKBD - Purgatory Pack - MiniLoop 05.ogg",
    "assets/MUSIC/17 - DavidKBD - Purgatory Pack - MiniLoop 09.ogg",
    "assets/MUSIC/21 - DavidKBD - Purgatory Pack - MiniLoop 13.ogg",
    "assets/MUSIC/22 - DavidKBD - Purgatory Pack - MiniLoop 14.ogg"
]

# ========================
# DEBUG SETTINGS
# ========================
# Debug settings
_DEBUG_MODE = os.getenv('ARCADE_DEBUG', 'False').lower() in ('true', '1', 't')
DEBUG_SHOW_HITBOXES = _DEBUG_MODE
DEBUG_SHOW_VECTORS = _DEBUG_MODE
DEBUG_SHOW_ANIM_STATES = _DEBUG_MODE

def set_debug_mode(enabled: bool):
    """Toggle debug mode at runtime"""
    global _DEBUG_MODE, DEBUG_SHOW_HITBOXES, DEBUG_SHOW_VECTORS, DEBUG_SHOW_ANIM_STATES
    _DEBUG_MODE = enabled
    DEBUG_SHOW_HITBOXES = enabled
    DEBUG_SHOW_VECTORS = enabled
    DEBUG_SHOW_ANIM_STATES = enabled

def get_debug_mode() -> bool:
    """Get current debug mode state"""
    return _DEBUG_MODE

DEBUG_MODE = property(get_debug_mode, set_debug_mode)
DEBUG_TEXT_COLOR = arcade.color.RED
DEBUG_TEXT_POSITION = (10, 10)

# ========================
# FUNCTIONS
# ========================
def set_resolution(res_key: str):
    """Update resolution and dependent constants"""
    global SCREEN_WIDTH, SCREEN_HEIGHT, _CURRENT_RESOLUTION, HEALTHBAR_PLAYER2_X
    if res_key in RESOLUTIONS:
        _CURRENT_RESOLUTION = res_key
        SCREEN_WIDTH, SCREEN_HEIGHT = RESOLUTIONS[res_key]
        # Update resolution-dependent UI positions
        HEALTHBAR_PLAYER2_X = SCREEN_WIDTH - 50 - HEALTHBAR_WIDTH