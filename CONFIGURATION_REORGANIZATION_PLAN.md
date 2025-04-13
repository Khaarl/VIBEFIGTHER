# Configuration Reorganization Plan

## Overview
This document outlines the reorganization of all game configuration into constants.py following best practices.

## New File Structure
```python
# arcade_fighter/src/constants.py
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
    "arcade_fighter/assets/MUSIC/09 - DavidKBD - Purgatory Pack - MiniLoop 01.ogg",
    # ... other music files
]

# ========================
# DEBUG SETTINGS
# ========================
DEBUG_MODE = os.getenv('ARCADE_DEBUG', 'False').lower() in ('true', '1', 't')
DEBUG_SHOW_HITBOXES = DEBUG_MODE
DEBUG_SHOW_VECTORS = DEBUG_MODE
DEBUG_SHOW_ANIM_STATES = DEBUG_MODE
DEBUG_TEXT_COLOR = arcade.color.RED
DEBUG_TEXT_POSITION = (10, 10)

# ========================
# FUNCTIONS
# ========================
def set_resolution(res_key: str):
    """Update resolution and dependent constants"""
    global SCREEN_WIDTH, SCREEN_HEIGHT, _CURRENT_RESOLUTION
    if res_key in RESOLUTIONS:
        _CURRENT_RESOLUTION = res_key
        SCREEN_WIDTH, SCREEN_HEIGHT = RESOLUTIONS[res_key]
        # Update resolution-dependent UI positions
        HEALTHBAR_PLAYER2_X = SCREEN_WIDTH - 50 - HEALTHBAR_WIDTH
```

## Implementation Steps
1. Replace contents of constants.py with the above
2. Update character.py to use the new constants:
   - Remove hardcoded attack values
   - Use CHARACTER_SCALING_BY_RESOLUTION
3. Update game_view.py to:
   - Use BACKGROUND_COLOR constant
   - Use health bar color constants
   - Remove hardcoded debug colors

## Verification
After implementation:
1. Test resolution changes
2. Verify all gameplay parameters work as expected
3. Check UI elements render correctly
4. Confirm debug functionality works