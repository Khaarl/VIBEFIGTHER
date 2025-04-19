import arcade
from .base_game_view import BaseGameView
from .. import constants as C
from .start_view import StartView # Import StartView for returning to main menu

class DebugGameView(BaseGameView):
    """Simplified view for animation testing"""
    
    def __init__(self):
        super().__init__()
        self.keys_pressed = set()
        self.menu_open = False
        self.menu_options = ["Return to Main Menu", "Select Character (Placeholder)", "Toggle Debug Visualizations"]
        
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
        """Render the screen with debug visualizations and menu."""
        # Call the base class's on_draw for common drawing
        super().on_draw()
        
        # Debug visualizations (controlled by flags in constants.py)
        if C.DEBUG_MODE: # Only draw debug visualizations if debug mode is on
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

        # Draw the menu if it's open
        if self.menu_open:
            # Draw a semi-transparent background
            # Draw a solid black background rectangle
            menu_width = C.SCREEN_WIDTH * 0.6
            menu_height = C.SCREEN_HEIGHT * 0.6
            center_x = C.SCREEN_WIDTH / 2
            center_y = C.SCREEN_HEIGHT / 2
            left = center_x - menu_width / 2
            right = center_x + menu_width / 2
            top = center_y + menu_height / 2
            bottom = center_y - menu_height / 2
            arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.BLACK)

            # Draw menu options
            menu_start_y = C.SCREEN_HEIGHT / 2 + (len(self.menu_options) - 1) * C.BUTTON_SPACING / 2
            for i, option in enumerate(self.menu_options):
                y = menu_start_y - i * C.BUTTON_SPACING
                arcade.draw_text(option, C.SCREEN_WIDTH / 2, y,
                                 arcade.color.WHITE, font_size=C.FONT_SIZE_BUTTON,
                                 anchor_x="center", anchor_y="center")
        
    def on_key_press(self, key, modifiers):
        """Handle key presses for animation testing and menu."""
        # Toggle menu on Escape key press
        if key == arcade.key.ESCAPE:
            self.menu_open = not self.menu_open
            # If menu is opened, pause the game (optional, depending on desired behavior)
            # if self.menu_open:
            #     self.window.set_update_rate(0) # Pause updates
            # else:
            #     self.window.set_update_rate(1/60) # Resume updates
            return # Consume the key press so it doesn't affect game if menu is open

        if self.menu_open:
            # Handle key presses within the menu (e.g., navigation)
            pass # Not implementing menu navigation with keys for now
        else:
            # Handle player controls via the base class and key map
            if not self.player1: # Check if player1 exists
                return

            self.keys_pressed.add(key)
            super().on_key_press(key, modifiers)
            
    def on_key_release(self, key, modifiers):
        """Handle key releases"""
        if self.menu_open:
            # Handle key releases within the menu
            pass
        else:
            if not self.player1: # Check if player1 exists
                return

            # Keep track of pressed keys for debug display
            if key in self.keys_pressed:
                self.keys_pressed.remove(key)

            # Handle player controls via the base class and key map
            super().on_key_release(key, modifiers)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse presses for menu interaction."""
        if self.menu_open:
            # Check if a menu option was clicked
            menu_start_y = C.SCREEN_HEIGHT / 2 + (len(self.menu_options) - 1) * C.BUTTON_SPACING / 2
            for i, option in enumerate(self.menu_options):
                option_y = menu_start_y - i * C.BUTTON_SPACING
                # Simple bounding box check for menu options (adjust as needed)
                if (C.SCREEN_WIDTH / 2 - 200 < x < C.SCREEN_WIDTH / 2 + 200 and
                    option_y - C.FONT_SIZE_BUTTON < y < option_y + C.FONT_SIZE_BUTTON):
                    
                    if i == 0: # Return to Main Menu
                        from .start_view import StartView
                        start_view = StartView()
                        self.window.show_view(start_view)
                    elif i == 1: # Select Character (Placeholder)
                        print("Select Character option clicked (Placeholder)")
                        # TODO: Implement character selection view
                        pass
                    elif i == 2: # Toggle Debug Visualizations
                        C.DEBUG_SHOW_HITBOXES = not C.DEBUG_SHOW_HITBOXES
                        C.DEBUG_SHOW_VECTORS = not C.DEBUG_SHOW_VECTORS
                        print(f"Debug Visualizations Toggled: Hitboxes={C.DEBUG_SHOW_HITBOXES}, Vectors={C.DEBUG_SHOW_VECTORS}")
                    
                    self.menu_open = False # Close menu after selection
                    # if not self.menu_open:
                    #     self.window.set_update_rate(1/60) # Resume updates
                    return # Consume the mouse press

        # If menu is not open, pass the event to the base class (for potential future use)
        # super().on_mouse_press(x, y, button, modifiers) # Uncomment if base class needs mouse press