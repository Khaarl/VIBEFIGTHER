import arcade
from arcade import hitbox
from typing import Tuple

def load_texture_pair(file_path: str) -> Tuple[arcade.Texture, arcade.Texture]:
    """
    Load a texture pair, with the second being a mirror image.
    Replaces the removed arcade.load_texture_pair() function.
    """
    texture = arcade.load_texture(file_path)
    flipped_texture = texture.flip_horizontally()
    return texture, flipped_texture
from . import constants as C

# Import states from constants
from .constants import (
    RIGHT_FACING,
    LEFT_FACING,
    STATE_IDLE,
    STATE_WALKING,
    STATE_JUMPING
)

STATE_FALLING = "falling" # New state not in constants


class Character(arcade.Sprite):
    """ Base Character class for players """
    def reload_textures(self):
        """Reload all character textures"""
        base_path = "arcade_fighter/assets/CHAR-ANIM/PLAYERS/EVil Wizard 2/Sprites/"
        
        # Load all textures
        self.idle_texture_pair = load_texture_pair(f"{base_path}Idle.png")
        self.walk_textures = [load_texture_pair(f"{base_path}Run.png")]
        self.jump_texture_pair = load_texture_pair(f"{base_path}Jump.png")
        self.fall_texture_pair = load_texture_pair(f"{base_path}Fall.png")
        self.attack_textures = [
            load_texture_pair(f"{base_path}Attack1.png"),
            load_texture_pair(f"{base_path}Attack2.png")
        ]
        
        # Reset current texture
        self.texture = self.idle_texture_pair[self.facing_direction]

    def attack(self):
        """Perform attack action"""
        if hasattr(self, 'is_attacking') and self.is_attacking:
            return
            
        self.is_attacking = True
        self.state = C.STATE_ATTACKING
        self.attack_frame = 0
        self.attack_timer = 0.0
        
        # Set initial attack texture
        self.texture = self.attack_textures[0][self.facing_direction]
        
    def __init__(self, player_num: int, scale: float = None):
        """Initialize character with optional scale.
        If scale is None, will calculate based on resolution."""
        if scale is None:
            # Use predefined scaling based on resolution
            scale = C.CHARACTER_SCALING_BY_RESOLUTION[C._CURRENT_RESOLUTION]
        super().__init__(scale=scale)

        # --- Player Identity ---
        self.player_num = player_num

        # --- State and Animation ---
        self.state = STATE_IDLE
        self.previous_state = STATE_IDLE
        self.facing_direction = RIGHT_FACING
        
        # Load textures
        self.reload_textures()
        
        # Set hit box (adjust as needed)
        self.hit_box = hitbox.HitBox(self.texture.hit_box_points)

        # --- Physics / Movement ---
        # self.change_x and self.change_y are inherited from Sprite
        self.is_on_ground = False # Will be updated by physics engine checks

        # --- Timers ---
        self.state_timer = 0.0

        if C.DEBUG_MODE:
            print(f"Character {player_num} created.")

    def update_animation(self, delta_time: float = 1/60):
        """
        Logic for selecting the proper texture to use.
        Also flips textures based on facing direction.
        """
        # Update animation every frame
        # Flip texture if direction changed
        if self.change_x < 0:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0:
            self.facing_direction = RIGHT_FACING

        # Update state based on physics
        new_state = self.state
        if not self.is_on_ground:
            if self.change_y > 0:
                new_state = STATE_JUMPING
            else:
                new_state = STATE_FALLING
        elif abs(self.change_x) > 0:
            new_state = STATE_WALKING
        else:
            new_state = STATE_IDLE
            
        # Track state transitions
        if new_state != self.state:
            self.previous_state = self.state
            self.state = new_state

        # Update texture based on state
        if self.state == STATE_IDLE:
            self.texture = self.idle_texture_pair[self.facing_direction]
        elif self.state == STATE_WALKING:
            self.texture = self.walk_textures[0][self.facing_direction]
        elif self.state == STATE_JUMPING:
            self.texture = self.jump_texture_pair[self.facing_direction]
        elif self.state == STATE_FALLING:
            self.texture = self.fall_texture_pair[self.facing_direction]

    def on_update(self, delta_time: float = 1/60):
        # Update any timers
        if self.state_timer > 0:
            self.state_timer -= delta_time
            # Handle timer expiration
            if self.state_timer <= 0:
                self.state_timer = 0


    def move(self, direction: int):
        """ Set horizontal movement speed based on direction (-1 left, 1 right) """
        self.change_x = C.PLAYER_MOVEMENT_SPEED * direction
        if self.is_on_ground:
            self.state = STATE_WALKING
        if C.DEBUG_MODE:
            print(f"Player {self.player_num} MOVING: direction={direction}, change_x={self.change_x}")

    def stop_moving(self):
        """ Stop horizontal movement """
        self.change_x = 0
        if self.is_on_ground:
            self.state = STATE_IDLE
        if C.DEBUG_MODE:
            print(f"Player {self.player_num} STOPPED MOVING")

    def jump(self):
        """ Initiate a jump if on the ground """
        if self.is_on_ground:
            self.change_y = C.PLAYER_JUMP_SPEED
            self.state = STATE_JUMPING
            self.is_on_ground = False # Assume we left the ground
            if C.DEBUG_MODE:
                print(f"Player {self.player_num} JUMP! change_y={self.change_y}")
        elif C.DEBUG_MODE:
            print(f"Player {self.player_num} JUMP ATTEMPTED BUT NOT GROUNDED")
