import arcade
from .base_game_view import BaseGameView
from .. import constants as C

class DebugGameView(BaseGameView):
    """Simplified view for animation testing"""
    
    def __init__(self):
        super().__init__()
        self.keys_pressed = set()
        
    def setup(self):
        """Set up the testing environment"""
        # Simple black background
        arcade.set_background_color(arcade.color.BLACK)
        
        # Setup common environment with single player
        super().setup_environment(player_count=1)
        # self.player1 is already available from BaseGameView

        if C.DEBUG_MODE:
            print("DebugGameView setup complete")
            if self.player1:
                print(f"Player position: ({self.player1.center_x}, {self.player1.center_y})")

        # --- Setup Key Mappings for Debug ---
        if self.player1:
            self.key_map_press[arcade.key.LEFT] = (self.player1, 'move', (-1,))
            self.key_map_press[arcade.key.RIGHT] = (self.player1, 'move', (1,))
            self.key_map_press[arcade.key.UP] = (self.player1, 'jump', ())
            self.key_map_press[arcade.key.SPACE] = (self.player1, 'attack', ()) # Assuming SPACE is attack

            self.key_map_release[arcade.key.LEFT] = (self.player1, 'stop_moving', ())
            self.key_map_release[arcade.key.RIGHT] = (self.player1, 'stop_moving', ())
        
    def on_draw(self):
        """Render the screen"""
        self.clear()
        self.platform_list.draw()
        self.player_list.draw()
        
        # Debug visualizations
        if C.DEBUG_SHOW_HITBOXES:
            for sprite in self.player_list:
                arcade.draw_polygon_outline(sprite.hit_box.get_adjusted_points(),
                                          arcade.color.RED, 1)
            for platform in self.platform_list:
                arcade.draw_polygon_outline(platform.hit_box.get_adjusted_points(),
                                          arcade.color.BLUE, 1)
        
        if C.DEBUG_SHOW_VECTORS:
            for sprite in self.player_list:
                # Draw velocity vector
                arcade.draw_line(sprite.center_x, sprite.center_y,
                               sprite.center_x + sprite.change_x * 5,
                               sprite.center_y + sprite.change_y * 5,
                               arcade.color.GREEN, 2)
                # Draw facing direction indicator
                arcade.draw_line(sprite.center_x, sprite.center_y,
                               sprite.center_x + sprite.facing_direction * 30,
                               sprite.center_y,
                               arcade.color.YELLOW, 2)
        
    def on_key_press(self, key, modifiers):
        """Handle key presses for animation testing"""
        if not self.player1: # Check if player1 exists
            return

        self.keys_pressed.add(key)

        # Handle player controls via the base class and key map
        super().on_key_press(key, modifiers)
            
    def on_key_release(self, key, modifiers):
        """Handle key releases"""
        if not self.player1: # Check if player1 exists
            return

        # Keep track of pressed keys for debug display
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

        # Handle player controls via the base class and key map
        super().on_key_release(key, modifiers)
            
    def on_update(self, delta_time):
        """Game logic updates, including base updates and debug logging"""
        if not self.player1 or not self.physics_engines: # Ensure player and engines exist
            return

        # Call base class update logic (handles physics, player animations, player logic)
        super().on_update(delta_time)

        # Get the physics engine for player 1
        physics_engine_p1 = self.physics_engines[0]

        # Detailed debug logging
        if C.DEBUG_MODE:
            print(f"\n--- Frame Update ---")
            print(f"State: {self.player1.state}")
            print(f"Position: ({self.player1.center_x:.1f}, {self.player1.center_y:.1f})")
            print(f"Velocity: (X:{self.player1.change_x:.1f}, Y:{self.player1.change_y:.1f})")
            print(f"On ground: {physics_engine_p1.can_jump()}")
            print(f"Keys pressed: {self.keys_pressed}")

            # Physics debug info
            if hasattr(self.player1, 'is_on_ground'):
                print(f"Ground state: {self.player1.is_on_ground}")

            # Collision checks
            if hasattr(physics_engine_p1, 'check_for_collision'):
                # Note: check_for_collision might not be a public method or might work differently
                # This part might need adjustment based on Arcade's API or intended use
                try:
                    collisions = physics_engine_p1.check_for_collision()
                    if collisions:
                        print(f"Collisions: {len(collisions)}")
                        for i, collision in enumerate(collisions[:3], 1):
                            print(f"  Collision {i}: {collision}")
                except AttributeError:
                     print("Debug: physics_engine has no 'check_for_collision' method.")


            # State transition info
            if hasattr(self.player1, 'previous_state'):
                if self.player1.previous_state != self.player1.state:
                    print(f"State changed from {self.player1.previous_state} to {self.player1.state}")