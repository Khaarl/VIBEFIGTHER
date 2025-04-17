import arcade
from arcade import hitbox
from typing import Tuple

def load_texture_pair(file_path: str) -> Tuple[arcade.Texture, arcade.Texture]:
    """
    Load a texture pair, with the second being a mirror image.
    Replaces the removed arcade.load_texture_pair() function.
    """
    # Basic error handling for file not found
    try:
        texture = arcade.load_texture(file_path)
        flipped_texture = texture.flip_horizontally()
        return texture, flipped_texture
    except FileNotFoundError:
        print(f"Error: Texture file not found at {file_path}")
        # Return placeholder textures or raise an error
        # For now, returning None to indicate failure
        return None, None
    except Exception as e:
        print(f"Error loading texture {file_path}: {e}")
        return None, None

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
    STATE_DEAD,
    # Animation timing
    UPDATES_PER_FRAME_WALK,
    UPDATES_PER_FRAME_ATTACK,
    UPDATES_PER_FRAME_HIT,
    UPDATES_PER_FRAME_DEATH
)


class Character(arcade.Sprite):
    """ Base Character class for players """
    def reload_textures(self):
        """Reload all character textures"""
        # TODO: Make base_path dynamic based on selected character
        base_path = "arcade_fighter/assets/CHAR-ANIM/PLAYERS/EVil Wizard 2/Sprites/"

        # Load all textures, handling potential loading failures
        self.idle_texture_pair = load_texture_pair(f"{base_path}Idle.png")
        # Assuming walk animation might have multiple frames eventually, but AssetManager needs update
        # For now, load Run.png as the single frame for walk
        walk_frame = load_texture_pair(f"{base_path}Run.png")
        self.walk_textures = [walk_frame] if walk_frame[0] else [] # Store as list even if single frame

        self.jump_texture_pair = load_texture_pair(f"{base_path}Jump.png")
        self.fall_texture_pair = load_texture_pair(f"{base_path}Fall.png")

        # Load attack frames, handling potential failures
        attack1 = load_texture_pair(f"{base_path}Attack1.png")
        attack2 = load_texture_pair(f"{base_path}Attack2.png")
        self.attack_textures = []
        if attack1[0]: self.attack_textures.append(attack1)
        if attack2[0]: self.attack_textures.append(attack2)

        hit_frame = load_texture_pair(f"{base_path}Take hit.png")
        self.hit_textures = [hit_frame] if hit_frame[0] else []

        death_frame = load_texture_pair(f"{base_path}Death.png")
        self.death_textures = [death_frame] if death_frame[0] else []

        # Reset current texture only if idle texture loaded successfully
        if self.idle_texture_pair[0]:
            self.texture = self.idle_texture_pair[self.facing_direction]
        else:
            # Handle case where even idle texture failed to load
            print(f"CRITICAL ERROR: Failed to load idle texture for character.")
            # Assign a default placeholder texture if available, or raise error
            # self.texture = arcade.make_placeholder_texture(...)
            pass # Or raise Exception("Failed to load essential character textures")


    def attack(self):
        """Perform attack action"""
        # TODO: Check cooldown timer
        if self.state in [STATE_ATTACKING, STATE_HIT, STATE_DEAD]: # Prevent attacking while in these states
            return

        if not self.attack_textures: # Don't attack if no animation loaded
             print(f"Warning: Player {self.player_num} cannot attack - missing textures.")
             return

        self.state = STATE_ATTACKING
        self.cur_texture_index = 0 # Reset animation index for attack
        self.texture_update_timer = 0.0
        # Set initial attack texture immediately
        self.texture = self.attack_textures[0][self.facing_direction]
        # TODO: Start attack cooldown timer

    def take_hit(self):
        """Handle taking a hit"""
        if self.state == STATE_DEAD: # Can't get hit if already dead
            return

        if not self.hit_textures: # Don't show hit anim if missing
             print(f"Warning: Player {self.player_num} cannot show hit - missing textures.")
             # Still apply damage etc.
             # TODO: Apply damage, check for death
             return # Skip animation part if no textures

        self.state = STATE_HIT
        self.cur_texture_index = 0
        self.texture_update_timer = 0.0
        # Set initial hit texture immediately
        self.texture = self.hit_textures[0][self.facing_direction]
        # TODO: Apply damage, check for death, maybe add brief stun/invulnerability timer

    def die(self):
        """Handle character death"""
        if self.state == STATE_DEAD: # Already dead
            return

        self.state = STATE_DEAD
        self.cur_texture_index = 0
        self.texture_update_timer = 0.0
        # Set initial death texture immediately
        if self.death_textures:
            self.texture = self.death_textures[0][self.facing_direction]
        else:
             print(f"Warning: Player {self.player_num} cannot show death - missing textures.")
        # TODO: Stop movement? Disable input? Signal game over?

    def __init__(self, player_num: int, scale: float = None):
        """Initialize character with optional scale.
        If scale is None, will calculate based on resolution."""
        if scale is None:
            # Use predefined scaling based on resolution
            scale = C.CHARACTER_SCALING_BY_RESOLUTION[C._CURRENT_RESOLUTION]
        
        # Initialize parent Sprite class first
        super().__init__(filename=None, scale=scale)
        
        # Ensure required attributes exist
        if not hasattr(self, '_position'):
            self._position = [0.0, 0.0]
        if not hasattr(self, '_angle'):
            self._angle = 0.0

        # --- Player Identity ---
        self.player_num = player_num

        # --- State and Animation ---
        self.state = STATE_IDLE
        self.previous_state = STATE_IDLE
        self.facing_direction = RIGHT_FACING
        self.cur_texture_index = 0 # Index for current frame in animated textures
        self.texture_update_timer = 0.0 # Timer to control animation speed

        # Load textures
        self.reload_textures() # This sets self.texture

        # Set hit box (adjust as needed)
        # Ensure texture is loaded before accessing hit_box_points
        if self.texture:
            try:
                self.hit_box = hitbox.HitBox(self.texture.hit_box_points)
            except Exception as e:
                 print(f"Error creating hitbox for Player {player_num}: {e}")
                 # Fallback hitbox
                 points = ((-22,-64), (22,-64), (22,28), (-22,28))
                 self.hit_box = hitbox.HitBox(points)
        else:
            # Fallback or error handling if texture loading failed
            print(f"Warning: Player {player_num} texture not loaded for hitbox init.")
            # Create a default small hitbox or handle error appropriately
            points = ((-22,-64), (22,-64), (22,28), (-22,28))
            self.hit_box = hitbox.HitBox(points)


        # --- Physics / Movement ---
        # self.change_x and self.change_y are inherited from Sprite
        self.is_on_ground = False # Will be updated by physics engine checks

        # --- Timers ---
        # Jump input buffering
        self.jump_pressed_time = 0.0
        self.jump_buffer_time = 0.1  # 100ms buffer window

        self.state_timer = 0.0 # Generic timer, might need more specific ones (attack cooldown, hit stun)

        if C.DEBUG_MODE:
            print(f"Character {player_num} created.")

    def update_animation(self, delta_time: float = 1/60):
        """
        Logic for selecting the proper texture to use, handling state transitions,
        cycling through animation frames, and flipping textures based on direction.
        """
        # --- Determine Facing Direction ---
        # Only change facing direction if not in a state that should lock direction
        if self.state not in [STATE_ATTACKING, STATE_HIT, STATE_DEAD]:
            if self.change_x < 0:
                self.facing_direction = LEFT_FACING
            elif self.change_x > 0:
                self.facing_direction = RIGHT_FACING

        # --- Determine Physics-Based State (potential state if not in action) ---
        current_physics_state = STATE_IDLE # Default
        if not self.is_on_ground:
            # Use a small tolerance for vertical velocity check near ground
            if self.change_y > 0.1:
                 current_physics_state = STATE_JUMPING
            else:
                 current_physics_state = STATE_JUMPING
        elif abs(self.change_x) > 0.1: # Use a small tolerance for horizontal movement
            current_physics_state = STATE_WALKING

        # --- State Transition Logic ---
        state_changed = False
        # Only transition TO physics state if not currently in a blocking action state
        if self.state not in [STATE_ATTACKING, STATE_HIT, STATE_DEAD]:
            if self.state != current_physics_state:
                self.previous_state = self.state
                self.state = current_physics_state
                state_changed = True
        # Note: Transitions INTO action states (attack, hit, dead) are handled by other methods

        # Reset animation index if state changed
        if state_changed:
            self.cur_texture_index = 0
            self.texture_update_timer = 0.0

        # --- Animation Frame Update ---
        self.texture_update_timer += delta_time

        # Select texture list and update speed based on state
        texture_list = None
        updates_per_frame = 5 # Default speed

        # Assign texture list based on current state, check if list exists
        if self.state == STATE_IDLE:
            if self.idle_texture_pair[0]: self.texture = self.idle_texture_pair[self.facing_direction]
            return # Idle has no frame sequence
        elif self.state == STATE_WALKING:
            if self.walk_textures: texture_list = self.walk_textures
            updates_per_frame = UPDATES_PER_FRAME_WALK
        elif self.state == STATE_JUMPING:
            if self.jump_texture_pair[0]: self.texture = self.jump_texture_pair[self.facing_direction]
            return # Jump has no frame sequence (usually)
            return # Fall has no frame sequence (usually)
        elif self.state == STATE_ATTACKING:
            if self.attack_textures: texture_list = self.attack_textures
            updates_per_frame = UPDATES_PER_FRAME_ATTACK
        elif self.state == STATE_HIT:
            if self.hit_textures: texture_list = self.hit_textures
            updates_per_frame = UPDATES_PER_FRAME_HIT
        elif self.state == STATE_DEAD:
            if self.death_textures: texture_list = self.death_textures
            updates_per_frame = UPDATES_PER_FRAME_DEATH
            # Keep showing last frame of death animation if already there and textures exist
            if texture_list and self.cur_texture_index >= len(texture_list) - 1:
                 self.texture = texture_list[-1][self.facing_direction]
                 return

        # --- Cycle Through Animation Frames ---
        if not texture_list: # If no textures for current state, fallback to idle
             if self.idle_texture_pair[0]: self.texture = self.idle_texture_pair[self.facing_direction]
             # Log warning if state should have had textures but didn't
             if self.state not in [STATE_IDLE, STATE_JUMPING]:
                 print(f"Warning: Missing textures for state {self.state}")
             return

        # Check if it's time to advance the frame
        frame_duration = updates_per_frame / 60.0
        if self.texture_update_timer >= frame_duration:
            self.texture_update_timer -= frame_duration # Subtract frame duration, don't just reset
            self.cur_texture_index += 1

            # Check if animation cycle finished
            if self.cur_texture_index >= len(texture_list):
                # Loop walking animation
                if self.state == STATE_WALKING:
                    self.cur_texture_index = 0
                # End attack/hit animation and return to appropriate physics state
                elif self.state in [STATE_ATTACKING, STATE_HIT]:
                    # Determine state to return to *after* action completes
                    if not self.is_on_ground:
                        next_state = STATE_JUMPING # Simplified: Use JUMPING for all airborne states
                    elif abs(self.change_x) > 0.1:
                        next_state = STATE_WALKING
                    else:
                        next_state = STATE_IDLE
                    self.state = next_state
                    self.cur_texture_index = 0 # Reset index for the new state's animation
                    # Update texture immediately based on new state
                    self.update_animation(0) # Call again immediately to set correct texture for new state
                    return # Exit after state change
                # Keep showing last frame for death
                elif self.state == STATE_DEAD:
                    self.cur_texture_index = len(texture_list) - 1
                else: # Default loop for any other multi-frame animations
                     self.cur_texture_index = 0

            # Set the texture for the current frame (or clamped index for death)
            frame_index = min(self.cur_texture_index, len(texture_list) - 1)
            if frame_index < len(texture_list): # Ensure index is valid
                self.texture = texture_list[frame_index][self.facing_direction]


    def on_update(self, delta_time: float = 1/60):
        # Update any timers (example: attack cooldown, hit stun)
        # This method might need more specific logic based on game needs
        if self.state_timer > 0:
            self.state_timer -= delta_time
            if self.state_timer <= 0:
                self.state_timer = 0
                # Example: End hit stun
                # if self.state == STATE_HIT:
                #     # Transition back to physics state handled by update_animation ending the cycle
                #     pass


    def move(self, direction: int):
        """ Set horizontal movement speed based on direction (-1 left, 1 right) """
        # Allow movement only if not in a blocking state
        if self.state not in [STATE_ATTACKING, STATE_HIT, STATE_DEAD]:
            self.change_x = C.PLAYER_MOVEMENT_SPEED * direction
            # State change to walking is handled in update_animation based on change_x
            if C.DEBUG_MODE:
                print(f"Player {self.player_num} MOVING: direction={direction}, change_x={self.change_x}")

    def stop_moving(self):
        """ Stop horizontal movement """
        # Only change speed if not in a blocking state where movement might be part of the animation
        if self.state not in [STATE_ATTACKING, STATE_HIT, STATE_DEAD]:
            self.change_x = 0
            # State change to idle is handled in update_animation based on change_x
            if C.DEBUG_MODE:
                print(f"Player {self.player_num} STOPPED MOVING")


    def jump(self):
        """ Initiate a jump if on the ground or within buffer window """
        # Record jump input time
        self.jump_pressed_time = 0.0  # Reset buffer timer
        
        # Check if we can jump now
        if (self.is_on_ground or self.jump_pressed_time < self.jump_buffer_time) and \
           self.state not in [STATE_ATTACKING, STATE_HIT, STATE_DEAD]:
            self.change_y = C.PLAYER_JUMP_SPEED
            self.is_on_ground = False
            self.jump_pressed_time = self.jump_buffer_time  # Prevent double jumps
            if C.DEBUG_MODE:
                print(f"Player {self.player_num} JUMP! change_y={self.change_y}")
        elif C.DEBUG_MODE:
            if not self.is_on_ground:
                 print(f"Player {self.player_num} JUMP ATTEMPTED BUT NOT GROUNDED")
            else:
                 print(f"Player {self.player_num} JUMP ATTEMPTED BUT IN STATE {self.state}")

    def on_update(self, delta_time: float = 1/60):
        """Update jump buffer timer"""
        if self.jump_pressed_time < self.jump_buffer_time:
            self.jump_pressed_time += delta_time
