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
    STATE_JUMPING,
    STATE_ATTACKING,
    STATE_HIT,
    STATE_DEAD
)

STATE_FALLING = "falling" # New state not in constants


class Character(arcade.Sprite):
    """ Base Character class for players """
    def reload_textures(self):
        """Reload all character textures"""
        # Cache textures if not already loaded
        if not hasattr(self, '_textures_loaded'):
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
            self.hit_texture_pair = load_texture_pair(f"{base_path}Take hit.png")
            self.death_texture_pair = load_texture_pair(f"{base_path}Death.png")
            
            self._textures_loaded = True
        
        # Reset current texture
        self.texture = self.idle_texture_pair[self.facing_direction]
        
    def __init__(self, player_num: int, scale: float = None):
        """Initialize character with optional scale.
        If scale is None, will calculate based on resolution."""
        if scale is None:
            # Base scale on resolution - smaller screens get larger characters
            if C.SCREEN_WIDTH <= 800:  # SD
                scale = 1.2
            elif C.SCREEN_WIDTH <= 1280:  # HD
                scale = 1.0
            else:  # FHD+
                scale = 0.8
        super().__init__(scale=scale)

        # --- Player Identity ---
        self.player_num = player_num

        # --- Health ---
        self.max_hp = C.PLAYER_START_HP
        self.hp = C.PLAYER_START_HP

        # --- State and Animation ---
        self.state = STATE_IDLE
        self.facing_direction = RIGHT_FACING
        
        # Load Evil Wizard 2 textures
        base_path = "arcade_fighter/assets/CHAR-ANIM/PLAYERS/EVil Wizard 2/Sprites/"
        
        # Idle animation
        self.idle_texture_pair = load_texture_pair(f"{base_path}Idle.png")
        
        # Walk animation
        self.walk_textures = []
        self.walk_textures.append(load_texture_pair(f"{base_path}Run.png"))
        
        # Jump animation
        self.jump_texture_pair = load_texture_pair(f"{base_path}Jump.png")
        
        # Fall animation
        self.fall_texture_pair = load_texture_pair(f"{base_path}Fall.png")
        
        # Attack animations
        self.attack_textures = []
        self.attack_textures.append(load_texture_pair(f"{base_path}Attack1.png"))
        self.attack_textures.append(load_texture_pair(f"{base_path}Attack2.png"))
        
        # Hit animation
        self.hit_texture_pair = load_texture_pair(f"{base_path}Take hit.png")
        
        # Death animation
        self.death_texture_pair = load_texture_pair(f"{base_path}Death.png")
        
        # Set initial texture
        self.texture = self.idle_texture_pair[self.facing_direction]
        
        # Set hit box (adjust as needed)
        self.hit_box = hitbox.HitBox(self.texture.hit_box_points)

        # --- Physics / Movement ---
        # self.change_x and self.change_y are inherited from Sprite
        self.is_on_ground = False # Will be updated by physics engine checks

        # --- Combat ---
        self.has_hit = False # Tracks if attack has already hit
        self.attack_cooldown = 0.0
        self.attack_duration = 0.5 # How long attack state lasts
        self.attack_damage = 10
        # Attack hitbox definition (width, height, offset_x, offset_y)
        self.attack_hitbox = {
            'width': 60,
            'height': 100,
            'offset_x': 40,
            'offset_y': 0
        }

        # --- Timers ---
        self.state_timer = 0.0 # Generic timer for states like 'hit' or 'attacking'

        if C.DEBUG_MODE:
            print(f"Character {player_num} created.")

    def update_animation(self, delta_time: float = 1/60):
        """
        Logic for selecting the proper texture to use.
        Also flips textures based on facing direction.
        """
        # Flip texture if direction changed
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Update texture based on state
        if self.state == STATE_IDLE:
            self.texture = self.idle_texture_pair[self.facing_direction]
        elif self.state == STATE_WALKING:
            self.texture = self.walk_textures[0][self.facing_direction]
        elif self.state == STATE_JUMPING:
            self.texture = self.jump_texture_pair[self.facing_direction]
        elif self.state == STATE_FALLING:
            self.texture = self.fall_texture_pair[self.facing_direction]
        elif self.state == STATE_ATTACKING:
            # Cycle through attack textures
            attack_frame = int(self.state_timer / self.attack_duration * len(self.attack_textures))
            attack_frame = min(attack_frame, len(self.attack_textures) - 1)
            self.texture = self.attack_textures[attack_frame][self.facing_direction]
        elif self.state == STATE_HIT:
            self.texture = self.hit_texture_pair[self.facing_direction]
        elif self.state == STATE_DEAD:
            self.texture = self.death_texture_pair[self.facing_direction]

    def on_update(self, delta_time: float = 1/60):
        """ Called by the arcade engine to update sprite state """

        # Update timers
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time
        if self.state_timer > 0:
            self.state_timer -= delta_time
            if self.state_timer <= 0:
                # Reset state if timer runs out (e.g., after being hit or attacking)
                if self.state == STATE_HIT or self.state == STATE_ATTACKING:
                    self.state = STATE_IDLE # Or STATE_FALLING if in air

        # State transition logic
        if not self.is_on_ground and self.state not in (STATE_JUMPING, STATE_FALLING, STATE_ATTACKING, STATE_HIT, STATE_DEAD):
            self.state = STATE_FALLING
        elif self.is_on_ground and self.state == STATE_FALLING and self.change_y == 0:
            self.state = STATE_IDLE

        # Check if dead
        if self.hp <= 0 and self.state != STATE_DEAD:
            self.state = STATE_DEAD
            self.change_x = 0
            # Maybe change texture to a "defeated" pose
            if C.DEBUG_MODE:
                print(f"Player {self.player_num} is DEAD")

    def move(self, direction: int):
        """ Set horizontal movement speed based on direction (-1 left, 1 right) """
        if self.state != STATE_HIT and self.state != STATE_DEAD: # Can't move when hit or dead
            self.change_x = C.PLAYER_MOVEMENT_SPEED * direction
            # TODO: Set state to WALKING if on ground?

    def stop_moving(self):
        """ Stop horizontal movement """
        self.change_x = 0
        # TODO: Set state to IDLE if on ground?

    def jump(self):
        """ Initiate a jump if on the ground """
        # TODO: Check if on ground using physics engine info
        # if self.physics_engine.can_jump(): # Requires passing engine or checking flag
        if self.is_on_ground and self.state != STATE_HIT and self.state != STATE_DEAD:
             self.change_y = C.PLAYER_JUMP_SPEED
             self.state = STATE_JUMPING
             self.is_on_ground = False # Assume we left the ground
             if C.DEBUG_MODE:
                 print(f"Player {self.player_num} JUMP!")

    def attack(self):
        """ Initiate an attack """
        if self.attack_cooldown <= 0 and self.state not in [STATE_ATTACKING, STATE_HIT, STATE_DEAD]:
            if C.DEBUG_MODE:
                print(f"Player {self.player_num} ATTACK!")
            self.has_hit = False # Reset hit flag for new attack
            self.state = STATE_ATTACKING
            self.attack_cooldown = 1.0 # Example: 1 second cooldown
            self.state_timer = self.attack_duration # Attack state lasts for this duration
            # Stop horizontal movement during attack? Optional.
            # self.change_x = 0
            # TODO: Create/position the attack hitbox in GameView's update

    def take_damage(self, amount: int):
        """ Take damage, update health, and change state """
        if self.state != STATE_DEAD: # Can't take damage if already dead
            self.hp -= amount
            if C.DEBUG_MODE:
                print(f"Player {self.player_num} takes {amount} damage. HP: {self.hp}/{self.max_hp}")
            if self.hp <= 0:
                self.hp = 0
                self.state = STATE_DEAD
                # Potentially trigger death animation/sound
            else:
                self.state = STATE_HIT
                self.state_timer = 0.3 # Example: Stunned/hit for 0.3 seconds
                # Optional: Add knockback effect
                # self.change_x = -self.facing_direction * 5 # Knockback example