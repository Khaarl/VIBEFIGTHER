import arcade

# --- Screen Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Arcade Fighter"

# --- Scaling ---
CHARACTER_SCALING = 1
TILE_SCALING = 0.5 # Example if using tiles later

# --- Physics Constants ---
GRAVITY = 1.0
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20

# --- Colors ---
WHITE = arcade.color.WHITE
BLACK = arcade.color.BLACK
RED = arcade.color.RED
BLUE = arcade.color.BLUE
GREEN = arcade.color.GREEN

# --- Player Constants ---
PLAYER_START_HP = 100

# --- Game States (Optional, Views handle this mostly) ---
# Can be useful for internal logic within a view
STATE_IDLE = "idle"

# --- Game Flow Constants ---
ROUNDS_TO_WIN = 2


# --- UI Constants ---
HEALTHBAR_WIDTH = 200
HEALTHBAR_HEIGHT = 20
HEALTHBAR_OFFSET_Y = 30 # Offset from top of screen
HEALTHBAR_PLAYER1_X = 50
HEALTHBAR_PLAYER2_X = SCREEN_WIDTH - 50 - HEALTHBAR_WIDTH
HEALTH_COLOR = arcade.color.GREEN
HEALTH_BACKGROUND_COLOR = arcade.color.DARK_RED
UI_FONT_SIZE = 18

STATE_WALKING = "walking"
STATE_JUMPING = "jumping"
STATE_ATTACKING = "attacking"
STATE_HIT = "hit"
STATE_DEAD = "dead"

# --- Character Directions ---
RIGHT_FACING = 0
LEFT_FACING = 1


# --- Input Keys (Example Mapping) ---
# Player 1
KEY_UP_P1 = arcade.key.W
KEY_DOWN_P1 = arcade.key.S # Optional for crouching later
KEY_LEFT_P1 = arcade.key.A
KEY_RIGHT_P1 = arcade.key.D
KEY_JUMP_P1 = arcade.key.W # Often same as UP
KEY_ATTACK_P1 = arcade.key.SPACE

# Player 2
KEY_UP_P2 = arcade.key.UP
KEY_DOWN_P2 = arcade.key.DOWN # Optional
KEY_LEFT_P2 = arcade.key.LEFT
KEY_RIGHT_P2 = arcade.key.RIGHT
KEY_JUMP_P2 = arcade.key.UP # Often same as UP
KEY_ATTACK_P2 = arcade.key.ENTER # Or NUM_ENTER