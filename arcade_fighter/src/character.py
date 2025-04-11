import arcade
from . import constants as C

# Constants for facing direction
RIGHT_FACING = 0
LEFT_FACING = 1

# --- Player states ---
# (Duplicated from constants for now, might refactor later)
STATE_IDLE = "idle"
STATE_WALKING = "walking"
STATE_JUMPING = "jumping"
STATE_FALLING = "falling" # Added state
STATE_ATTACKING = "attacking"
STATE_HIT = "hit"
STATE_DEAD = "dead"


class Character(arcade.Sprite):
    """ Base Character class for players """
    def __init__(self, player_num: int, scale: float = 1):
        super().__init__(scale=scale)

        # --- Player Identity ---
        self.player_num = player_num

        # --- Health ---
        self.max_hp = C.PLAYER_START_HP
        self.hp = C.PLAYER_START_HP

        # --- State and Animation ---
        self.state = STATE_IDLE
        self.facing_direction = RIGHT_FACING # Default direction
        # TODO: Load textures here (idle, walk, jump, attack etc.)
        # Example: self.idle_texture_pair = arcade.load_texture_pair(f"path/to/idle.png")
        #          self.walk_textures = [...]
        # Use a simple colored box as a placeholder for now
        self.texture = arcade.make_soft_square_texture(50, C.RED if player_num == 1 else C.BLUE, center_alpha=255)
        # Placeholder size - adjust as needed
        self.width = self.texture.width * scale
        self.height = self.texture.height * scale


        # --- Physics / Movement ---
        # self.change_x and self.change_y are inherited from Sprite
        self.is_on_ground = False # Will be updated by physics engine checks

        # --- Combat ---
        self.has_hit = False # Tracks if attack has already hit
        self.attack_cooldown = 0.0
        self.attack_duration = 0.5 # How long attack state lasts
        self.attack_damage = 10
        # TODO: Define hitbox shape/offset relative to sprite center
        self.attack_hitbox = None # Will be a temporary sprite or rect during attack

        # --- Timers ---
        self.state_timer = 0.0 # Generic timer for states like 'hit' or 'attacking'

        print(f"Character {player_num} created.") # Debug print

    def update_animation(self, delta_time: float = 1/60):
        """
        Logic for selecting the proper texture to use.
        Also flips textures based on facing direction.
        """
        # --- Texture flipping based on facing direction ---
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # TODO: Add animation logic here based on self.state
        # Example:
        # if self.state == STATE_WALKING:
        #     self.texture = self.walk_textures[self.current_texture_index]
        # elif self.state == STATE_IDLE:
        #     self.texture = self.idle_texture_pair[self.facing_direction]
        # ... etc ...

        # For now, just ensure the placeholder texture is set
        # (It's set in __init__, so this might not be needed yet)
        # self.texture = self.texture # No real animation yet

        pass # Placeholder

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

        # TODO: Add state logic updates here
        # - Transition between states (e.g., jumping -> falling)
        # - Handle state-specific behavior

        # Check if dead
        if self.hp <= 0 and self.state != STATE_DEAD:
            self.state = STATE_DEAD
            self.change_x = 0
            # Maybe change texture to a "defeated" pose
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
             print(f"Player {self.player_num} JUMP!") # Debug

    def attack(self):
        """ Initiate an attack """
        if self.attack_cooldown <= 0 and self.state not in [STATE_ATTACKING, STATE_HIT, STATE_DEAD]:
            print(f"Player {self.player_num} ATTACK!") # Debug
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
            print(f"Player {self.player_num} takes {amount} damage. HP: {self.hp}/{self.max_hp}") # Debug
            if self.hp <= 0:
                self.hp = 0
                self.state = STATE_DEAD
                # Potentially trigger death animation/sound
            else:
                self.state = STATE_HIT
                self.state_timer = 0.3 # Example: Stunned/hit for 0.3 seconds
                # Optional: Add knockback effect
                # self.change_x = -self.facing_direction * 5 # Knockback example