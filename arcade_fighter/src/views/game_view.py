
import arcade
from .. import constants as C
from ..character import Character
# Import GameOverView later for transitions
# from .game_over_view import GameOverView

class GameView(arcade.View):
    """ Main application class where the fighting happens. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.player_list = None
        self.platform_list = None # For floor, etc.

        # Player sprites
        self.player1_sprite = None
        self.player2_sprite = None

        # Physics engine
        self.physics_engine_p1 = None
        self.physics_engine_p2 = None

        # Game state variables
        self.round_number = 1
        self.player1_rounds_won = 0
        self.player2_rounds_won = 0
        # Add more state as needed (timers, scores, etc.)

        # Set background color
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def debug_setup(self):
        """Simplified setup for debug mode"""
        # Clear existing sprites
        self.player_list.clear()
        self.platform_list.clear()
        
        # Create test platform
        platform = arcade.SpriteSolidColor(
            int(C.SCREEN_WIDTH * 1.5), 64, 
            arcade.color.GRAY
        )
        platform.center_x = C.SCREEN_WIDTH / 2
        platform.center_y = 32
        self.platform_list.append(platform)
        
        # Create only Player 1
        self.player1_sprite = Character(
            player_num=1, 
            scale=C.CHARACTER_SCALING
        )
        self.player1_sprite.center_x = C.SCREEN_WIDTH / 2
        self.player1_sprite.bottom = 64
        self.player_list.append(self.player1_sprite)
        
        # Simplified physics
        self.physics_engine_p1 = arcade.PhysicsEnginePlatformer(
            self.player1_sprite, 
            self.platform_list, 
            gravity_constant=C.GRAVITY
        )
        
    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        print("Setting up GameView...") # Debug print
        # Initialize sprite lists
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList(use_spatial_hash=True) # Spatial hash for static platforms

        # --- Background Setup ---
        self.background = arcade.load_texture(
            "arcade_fighter/assets/LEVELS/Glacial-mountains/background_glacial_mountains.png"
        )

                # --- Player Setup --- (Phase 3)
        # Player 1
        self.player1_sprite = Character(player_num=1, scale=C.CHARACTER_SCALING)
        self.player1_sprite.center_x = C.SCREEN_WIDTH * 0.25
        self.player1_sprite.bottom = 64 # Start on the floor (floor top is y=64)
        self.player_list.append(self.player1_sprite)

        # Player 2
        self.player2_sprite = Character(player_num=2, scale=C.CHARACTER_SCALING)
        self.player2_sprite.center_x = C.SCREEN_WIDTH * 0.75
        self.player2_sprite.bottom = 64 # Start on the floor
        self.player_list.append(self.player2_sprite)
# --- Floor Setup ---
        # Create the ground
        # TODO: Use actual coordinates and potentially a texture
        floor = arcade.SpriteSolidColor(int(C.SCREEN_WIDTH * 1.5), 64, arcade.color.DARK_SPRING_GREEN)
        floor.center_x = C.SCREEN_WIDTH / 2
        floor.center_y = 32 # Bottom half of the sprite is the ground level
        self.platform_list.append(floor)

                # --- Physics Engine Setup --- (Phase 5)
        if self.player1_sprite:
            self.physics_engine_p1 = arcade.PhysicsEnginePlatformer(
                self.player1_sprite, self.platform_list, gravity_constant=C.GRAVITY
            )
        if self.player2_sprite:
            self.physics_engine_p2 = arcade.PhysicsEnginePlatformer(
                self.player2_sprite, self.platform_list, gravity_constant=C.GRAVITY
            )
        # if self.player2_sprite:
        #     self.physics_engine_p2 = arcade.PhysicsEnginePlatformer(
        #         self.player2_sprite, self.platform_list, gravity_constant=C.GRAVITY
        #     )

        # Reset scores/rounds if needed for a full restart
        self.round_number = 1
        self.player1_rounds_won = 0
        self.player2_rounds_won = 0

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.update_viewport()
        # Potentially call setup() here if you want a fresh game every time
        # self.setup()

    def on_resize(self, width: int, height: int):
        """Handle window resize events"""
        super().on_resize(width, height)
        self.update_viewport()
        
    def update_viewport(self):
        """Update viewport and UI positions based on current resolution"""
        self.window.viewport = (0, 0, C.SCREEN_WIDTH, C.SCREEN_HEIGHT)
        # Update any resolution-dependent positions
        if hasattr(self, 'player1_sprite') and self.player1_sprite:
            self.player1_sprite.center_x = C.SCREEN_WIDTH * 0.25
        if hasattr(self, 'player2_sprite') and self.player2_sprite:
            self.player2_sprite.center_x = C.SCREEN_WIDTH * 0.75

    def debug_draw(self):
        """Draw debug overlays"""
        if C.DEBUG_SHOW_HITBOXES:
            for player in self.player_list:
                arcade.draw_polygon_outline(
                    player.hit_box.get_adjusted_points(),
                    arcade.color.RED,
                    2
                )
                
        if C.DEBUG_SHOW_VECTORS and self.player1_sprite:
            # Draw velocity vector
            arcade.draw_line(
                self.player1_sprite.center_x,
                self.player1_sprite.center_y,
                self.player1_sprite.center_x + self.player1_sprite.change_x * 10,
                self.player1_sprite.center_y + self.player1_sprite.change_y * 10,
                arcade.color.BLUE,
                2
            )
            
        if C.DEBUG_SHOW_ANIM_STATES and self.player1_sprite:
            arcade.draw_text(
                f"State: {self.player1_sprite.state}",
                self.player1_sprite.left,
                self.player1_sprite.top + 20,
                arcade.color.WHITE,
                12
            )
            
    def draw_debug_hud(self):
        """Draw debug information overlay"""
        if not C.DEBUG_MODE:
            return
            
        # Debug controls info
        debug_text = [
            "DEBUG MODE ACTIVATED",
            "F1: Toggle Debug",
            "F2: Toggle Hitboxes",
            "F3: Toggle Vectors",
            "F4: Toggle Anim States",
            "F5: Reload Assets"
        ]
        
        for i, text in enumerate(debug_text):
            arcade.draw_text(
                text,
                10, C.SCREEN_HEIGHT - 30 - (i * 20),
                arcade.color.RED if i == 0 else arcade.color.WHITE,
                12
            )
            
    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        
        # Draw debug HUD
        self.draw_debug_hud()
        
        if C.DEBUG_MODE:
            self.debug_draw()

        # Draw game elements
        if hasattr(self, 'background'):
            arcade.draw_lrwh_rectangle_textured(0, 0, C.SCREEN_WIDTH, C.SCREEN_HEIGHT, self.background)

        self.platform_list.draw()
        self.player_list.draw()

                # Draw UI elements (Phase 7)
        # --- Health Bars ---
        # Calculate health bar width based on current HP
        if self.player1_sprite:
            health_width_p1 = C.HEALTHBAR_WIDTH * (self.player1_sprite.hp / self.player1_sprite.max_hp)
            if health_width_p1 < 0: health_width_p1 = 0
            # Background
            arcade.draw_lrbt_rectangle_filled(left=C.HEALTHBAR_PLAYER1_X,
                                              right=C.HEALTHBAR_PLAYER1_X + C.HEALTHBAR_WIDTH,
                                              top=C.SCREEN_HEIGHT - C.HEALTHBAR_OFFSET_Y + C.HEALTHBAR_HEIGHT/2,
                                              bottom=C.SCREEN_HEIGHT - C.HEALTHBAR_OFFSET_Y - C.HEALTHBAR_HEIGHT/2,
                                              color=C.HEALTH_BACKGROUND_COLOR)
            # Health
            arcade.draw_lrbt_rectangle_filled(left=C.HEALTHBAR_PLAYER1_X,
                                              right=C.HEALTHBAR_PLAYER1_X + health_width_p1,
                                              top=C.SCREEN_HEIGHT - C.HEALTHBAR_OFFSET_Y + C.HEALTHBAR_HEIGHT/2,
                                              bottom=C.SCREEN_HEIGHT - C.HEALTHBAR_OFFSET_Y - C.HEALTHBAR_HEIGHT/2,
                                              color=C.HEALTH_COLOR)
            # Player 1 Text
            arcade.draw_text("Player 1", C.HEALTHBAR_PLAYER1_X, C.SCREEN_HEIGHT - C.HEALTHBAR_OFFSET_Y - 25, 
                             arcade.color.WHITE, C.UI_FONT_SIZE)

        if self.player2_sprite:
            health_width_p2 = C.HEALTHBAR_WIDTH * (self.player2_sprite.hp / self.player2_sprite.max_hp)
            if health_width_p2 < 0: health_width_p2 = 0
            # Background
            arcade.draw_lrbt_rectangle_filled(left=C.HEALTHBAR_PLAYER2_X,
                                              right=C.HEALTHBAR_PLAYER2_X + C.HEALTHBAR_WIDTH,
                                              top=C.SCREEN_HEIGHT - C.HEALTHBAR_OFFSET_Y + C.HEALTHBAR_HEIGHT/2,
                                              bottom=C.SCREEN_HEIGHT - C.HEALTHBAR_OFFSET_Y - C.HEALTHBAR_HEIGHT/2,
                                              color=C.HEALTH_BACKGROUND_COLOR)
            # Health
            arcade.draw_lrbt_rectangle_filled(left=C.HEALTHBAR_PLAYER2_X,
                                              right=C.HEALTHBAR_PLAYER2_X + health_width_p2,
                                              top=C.SCREEN_HEIGHT - C.HEALTHBAR_OFFSET_Y + C.HEALTHBAR_HEIGHT/2,
                                              bottom=C.SCREEN_HEIGHT - C.HEALTHBAR_OFFSET_Y - C.HEALTHBAR_HEIGHT/2,
                                              color=C.HEALTH_COLOR)
            # Player 2 Text
            arcade.draw_text("Player 2", C.HEALTHBAR_PLAYER2_X, C.SCREEN_HEIGHT - C.HEALTHBAR_OFFSET_Y - 25, 
                             arcade.color.WHITE, C.UI_FONT_SIZE)

        # --- Round Indicator ---
        arcade.draw_text(f"Round: {self.round_number}", C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT - C.HEALTHBAR_OFFSET_Y - 10,
                         arcade.color.WHITE, C.UI_FONT_SIZE, anchor_x="center")
        # TODO: Add round win indicators later
        arcade.draw_text("Game View - Placeholder", C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")


    def on_update(self, delta_time):
        """ Movement and game logic """
                # Update physics and ground state
        # Update player ground state
        if self.player1_sprite:
            self.player1_sprite.is_on_ground = self.physics_engine_p1.can_jump()
        if self.player2_sprite:
            self.player2_sprite.is_on_ground = self.physics_engine_p2.can_jump()
        if self.physics_engine_p1:
            self.physics_engine_p1.update()
        if self.physics_engine_p2:
            self.physics_engine_p2.update()

        # Update sprites (calls Character.on_update)
        self.player_list.update()
        # Update animations (calls Character.update_animation)
        self.player_list.update_animation(delta_time)


        # --- Collision Checks (Phase 5) ---
        # Boundary Checks
        for player in self.player_list:
            if player.left < 0:
                player.left = 0
            elif player.right > C.SCREEN_WIDTH:
                player.right = C.SCREEN_WIDTH
            # Add top/bottom checks if needed

        # Character-Character Collision
        if self.player1_sprite and self.player2_sprite:
            if arcade.check_for_collision(self.player1_sprite, self.player2_sprite):
                # Simple push-apart logic
                overlap_x = (self.player1_sprite.width / 2 + self.player2_sprite.width / 2) - abs(self.player1_sprite.center_x - self.player2_sprite.center_x)
                push_amount = overlap_x / 2

                if self.player1_sprite.center_x < self.player2_sprite.center_x:
                    # Player 1 is left, Player 2 is right
                    self.player1_sprite.center_x -= push_amount
                    self.player2_sprite.center_x += push_amount
                else:
                    # Player 1 is right, Player 2 is left
                    self.player1_sprite.center_x += push_amount
                    self.player2_sprite.center_x -= push_amount

                # Prevent sticking if moving towards each other
                # Optional: Adjust velocities as well, or just rely on position correction


        # --- Attack Checks (Phase 6) ---
        self.check_attacks()


        # --- Check Win/Loss Conditions (Phase 8) ---
        self.check_round_end()

        # TODO: Add game logic:
        # - Check for attacks/collisions (Phase 6)
        # - Check win/loss conditions (Phase 8)
        # - Handle character-character collision (Phase 5)
        # - Handle boundary checks (Phase 5)
        # - Handle AI if applicable (Phase 9)

                
    def reload_assets(self):
        """Hot-reload character assets"""
        if self.player1_sprite:
            self.player1_sprite.reload_textures()
            print("Assets reloaded")
            
    def on_key_press(self, key, modifiers):
        """Called when a key is pressed. """
        # Debug controls
        if C.DEBUG_MODE:
            if key == arcade.key.F1:
                C.DEBUG_MODE = not C.DEBUG_MODE
            elif key == arcade.key.F2:
                C.DEBUG_SHOW_HITBOXES = not C.DEBUG_SHOW_HITBOXES
            elif key == arcade.key.F3:
                C.DEBUG_SHOW_VECTORS = not C.DEBUG_SHOW_VECTORS
            elif key == arcade.key.F4:
                C.DEBUG_SHOW_ANIM_STATES = not C.DEBUG_SHOW_ANIM_STATES
            elif key == arcade.key.F5:
                self.reload_assets()
                return
        
        # Original controls
        # --- Player 1 Controls ---
        if self.player1_sprite:
            if key == C.KEY_JUMP_P1 and self.physics_engine_p1.can_jump():
                # TODO: Check physics engine can_jump() here later
                self.player1_sprite.jump()
            elif key == C.KEY_LEFT_P1:
                self.player1_sprite.move(-1)
            elif key == C.KEY_RIGHT_P1:
                self.player1_sprite.move(1)
            elif key == C.KEY_ATTACK_P1:
                self.player1_sprite.attack()
            # Add Down/Crouch later if needed
            # elif key == C.KEY_DOWN_P1:
            #     pass

        # --- Player 2 Controls ---
        if self.player2_sprite:
            if key == C.KEY_JUMP_P2 and self.physics_engine_p2.can_jump():
                # TODO: Check physics engine can_jump() here later
                self.player2_sprite.jump()
            elif key == C.KEY_LEFT_P2:
                self.player2_sprite.move(-1)
            elif key == C.KEY_RIGHT_P2:
                self.player2_sprite.move(1)
            elif key == C.KEY_ATTACK_P2:
                self.player2_sprite.attack()
            # Add Down/Crouch later if needed
            # elif key == C.KEY_DOWN_P2:
            #     pass

        # Temporary exit/reset
        if key == arcade.key.ESCAPE:
            arcade.exit()
        if key == arcade.key.R: # Temporary reset
            self.setup()


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        # --- Player 1 Movement Stop ---
        if self.player1_sprite:
            if key == C.KEY_LEFT_P1 and self.player1_sprite.change_x < 0:
                self.player1_sprite.stop_moving()
            elif key == C.KEY_RIGHT_P1 and self.player1_sprite.change_x > 0:
                self.player1_sprite.stop_moving()

        # --- Player 2 Movement Stop ---
        if self.player2_sprite:
            if key == C.KEY_LEFT_P2 and self.player2_sprite.change_x < 0:
                self.player2_sprite.stop_moving()
            elif key == C.KEY_RIGHT_P2 and self.player2_sprite.change_x > 0:
                self.player2_sprite.stop_moving()

    def check_attacks(self):
        """ Check if any player attacks hit the other player. """
        if not self.player1_sprite or not self.player2_sprite:
            return

        # Check Player 1 attacking Player 2
        if self.player1_sprite.state == C.STATE_ATTACKING and self.player1_sprite.state_timer > (self.player1_sprite.attack_duration - 0.1):
            # Simple hitbox in front of the player
            hitbox_width = 60
            hitbox_height = self.player1_sprite.height
            hitbox_offset_x = 40 # How far in front
            
            if self.player1_sprite.facing_direction == C.RIGHT_FACING:
                hitbox_center_x = self.player1_sprite.center_x + hitbox_offset_x
            else: # LEFT_FACING
                hitbox_center_x = self.player1_sprite.center_x - hitbox_offset_x
            hitbox_center_y = self.player1_sprite.center_y

            # Use pre-created hitbox if available, otherwise create
            if not hasattr(self, '_attack_hitbox'):
                self._attack_hitbox = arcade.SpriteSolidColor(60, 100, (0, 0, 0, 0))
            
            self._attack_hitbox.width = hitbox_width
            self._attack_hitbox.height = hitbox_height
            self._attack_hitbox.center_x = hitbox_center_x
            self._attack_hitbox.center_y = hitbox_center_y
            attack_hitbox = self._attack_hitbox
            
            if arcade.check_for_collision(attack_hitbox, self.player2_sprite):
                # Hit detected!
                # Prevent multiple hits per single attack animation/state
                # We can check if the attack timer is near its start
                if self.player1_sprite.state_timer > (self.player1_sprite.attack_duration - 0.1): # Allow hit near start of attack
                     print(f"HIT! Player 1 attacks Player 2")
                     self.player2_sprite.take_damage(self.player1_sprite.attack_damage)
                     # Optional: Reset state timer slightly to prevent immediate re-hit
                     # self.player1_sprite.state_timer = self.player1_sprite.attack_duration - 0.15 


        # Check Player 2 attacking Player 1 (similar logic)
        if self.player2_sprite.state == C.STATE_ATTACKING and self.player2_sprite.state_timer > (self.player2_sprite.attack_duration - 0.1):
            hitbox_width = 60
            hitbox_height = self.player2_sprite.height
            hitbox_offset_x = 40
            
            if self.player2_sprite.facing_direction == C.RIGHT_FACING:
                hitbox_center_x = self.player2_sprite.center_x + hitbox_offset_x
            else: # LEFT_FACING
                hitbox_center_x = self.player2_sprite.center_x - hitbox_offset_x
            hitbox_center_y = self.player2_sprite.center_y

            attack_hitbox = arcade.SpriteSolidColor(hitbox_width, hitbox_height, (0, 0, 0, 0)) # Transparent hitbox
            attack_hitbox.center_x = hitbox_center_x
            attack_hitbox.center_y = hitbox_center_y
            
            if arcade.check_for_collision(attack_hitbox, self.player1_sprite) and not self.player2_sprite.has_hit:
                if self.player2_sprite.state_timer > (self.player2_sprite.attack_duration - 0.1):
                     print(f"HIT! Player 2 attacks Player 1")
                     self.player1_sprite.take_damage(self.player2_sprite.attack_damage)
                     # Optional: Reset state timer slightly
                     # self.player2_sprite.state_timer = self.player2_sprite.attack_duration - 0.15

    def reset_round(self):
        """ Resets player positions and health for the next round. """
        print(f"Resetting for Round {self.round_number}")
        # Reset positions and health
        if self.player1_sprite:
            self.player1_sprite.center_x = C.SCREEN_WIDTH * 0.25
            self.player1_sprite.bottom = 64
            self.player1_sprite.hp = self.player1_sprite.max_hp
            self.player1_sprite.state = C.STATE_IDLE
            self.player1_sprite.change_x = 0
            self.player1_sprite.change_y = 0

        if self.player2_sprite:
            self.player2_sprite.center_x = C.SCREEN_WIDTH * 0.75
            self.player2_sprite.bottom = 64
            self.player2_sprite.hp = self.player2_sprite.max_hp
            self.player2_sprite.state = C.STATE_IDLE
            self.player2_sprite.change_x = 0
            self.player2_sprite.change_y = 0
        
        # Re-initialize physics engines with potentially reset sprites
        # (Might not be strictly necessary if only positions/velocities changed,
        # but safer to ensure correct state)
        if self.player1_sprite:
            self.physics_engine_p1 = arcade.PhysicsEnginePlatformer(
                self.player1_sprite, self.platform_list, gravity_constant=C.GRAVITY
            )
        if self.player2_sprite:
            self.physics_engine_p2 = arcade.PhysicsEnginePlatformer(
                self.player2_sprite, self.platform_list, gravity_constant=C.GRAVITY
            )

    def check_round_end(self):
        """ Check if a player's HP is 0 or less, handle round/match end. """
        round_winner = None
        if self.player1_sprite and self.player1_sprite.hp <= 0:
            round_winner = 2
            self.player2_rounds_won += 1
            print(f"Round {self.round_number} Winner: Player 2")
        elif self.player2_sprite and self.player2_sprite.hp <= 0:
            round_winner = 1
            self.player1_rounds_won += 1
            print(f"Round {self.round_number} Winner: Player 1")

        if round_winner:
            # Check if match is over
            if self.player1_rounds_won >= C.ROUNDS_TO_WIN or self.player2_rounds_won >= C.ROUNDS_TO_WIN:
                match_winner = 1 if self.player1_rounds_won > self.player2_rounds_won else 2
                print(f"Match Over! Winner: Player {match_winner}")
                from .game_over_view import GameOverView # Import here
                game_over_view = GameOverView(winner=match_winner)
                self.window.show_view(game_over_view)
            else:
                # Start next round
                self.round_number += 1
                # TODO: Add a brief pause/message before resetting
                self.reset_round()

