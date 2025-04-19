import arcade
from .base_game_view import BaseGameView
from .. import constants as C
from ..character import Character # Import Character
from .asset_manager import AssetManager # Import AssetManager
# from .start_view import StartView # Removed to fix circular import

class LevelTestView(BaseGameView):
    """View for testing level generation."""

    def __init__(self):
        super().__init__()
        super().__init__()
        self.level_generated = False # Flag to ensure level is generated only once
        self.background_layers = arcade.SpriteList() # Use SpriteList for background layers
        self.background_speeds = [] # List to hold speeds corresponding to background_layers
        self.asset_manager = AssetManager() # Initialize AssetManager

    def setup(self):
        """Set up the level generation testing environment."""
        super().setup_environment(player_count=0) # Start with no players initially

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # --- Load and Setup Background Layers (Parallax) ---
        background_layer_info = [
            ("assets/LEVELS/Glacial-mountains/Layers/sky.png", 0.1),
            ("assets/LEVELS/Glacial-mountains/Layers/glacial_mountains.png", 0.3),
            ("assets/LEVELS/Glacial-mountains/Layers/clouds_mg_3.png", 0.5),
            ("assets/LEVELS/Glacial-mountains/Layers/clouds_mg_2.png", 0.7),
            ("assets/LEVELS/Glacial-mountains/Layers/clouds_mg_1.png", 0.9),
            ("assets/LEVELS/Glacial-mountains/Layers/cloud_lonely.png", 1.0), # Example of a closer cloud
        ]

        for path, speed in background_layer_info:
            texture = self.asset_manager._load_texture(path)
            if texture: # Only create sprite if texture loaded successfully
                sprite = arcade.Sprite(texture)
                sprite.center_x = C.SCREEN_WIDTH / 2
                sprite.center_y = C.SCREEN_HEIGHT / 2
                # Scale sprite to cover the screen width, maintaining aspect ratio
                sprite.scale = C.SCREEN_WIDTH / sprite.width
                self.background_layers.append(sprite)
                self.background_speeds.append(speed)
            else:
                print(f"Warning: Could not load background texture: {path}")


        # --- Basic Level Generation for Testing ---
        print("LevelTestView setup: Generating a basic test level.")

        # Define a simple level structure (x, y, width, height)
        level_structure = [
            (C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT / 4, C.SCREEN_WIDTH * 0.8, 50),
            (C.SCREEN_WIDTH * 0.2, C.SCREEN_HEIGHT / 2, 200, 50),
            (C.SCREEN_WIDTH * 0.8, C.SCREEN_HEIGHT / 2, 200, 50),
            (C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT * 0.75, 400, 50),
        ]

        # Create platforms based on the level structure
        for center_x, center_y, width, height in level_structure:
            platform = arcade.SpriteSolidColor(width, height, arcade.color.DARK_GREEN)
            platform.center_x = center_x
            platform.center_y = center_y
            self.platform_list.append(platform)

        # Create a player
        self.player1 = Character(player_num=1, character_name="Medieval King Pack 2", scale=C.CHARACTER_SCALING)
        self.player1.center_x = C.SCREEN_WIDTH * 0.25
        self.player1.bottom = self.platform_list[0].top + 10 # Place on the first platform
        self.player_list.append(self.player1)

        # Setup physics engine for the player
        self.physics_engines.append(
            arcade.PhysicsEnginePlatformer(
                self.player1,
                self.platform_list,
                gravity_constant=C.GRAVITY
            )
        )

        self.level_generated = True

        # --- Setup Key Mappings for Player ---
        if self.player1:
            self.key_map_press[C.KEY_LEFT_P1] = (self.player1, 'move', (-1,))
            self.key_map_press[C.KEY_RIGHT_P1] = (self.player1, 'move', (1,))
            self.key_map_press[C.KEY_JUMP_P1] = (self.player1, 'jump', ())
            # Add attack key if defined in constants
            if hasattr(C, 'KEY_ATTACK_P1'):
                 self.key_map_press[C.KEY_ATTACK_P1] = (self.player1, 'attack', ())

            self.key_map_release[C.KEY_LEFT_P1] = (self.player1, 'stop_moving', ())
            self.key_map_release[C.KEY_RIGHT_P1] = (self.player1, 'stop_moving', ())


    def on_draw(self):
        """Render the level testing view."""
        self.clear()

        # Draw background layers first
        self.background_layers.draw()

        # Draw the generated level elements (platforms, etc.)
        if self.platform_list:
            self.platform_list.draw()
        # Draw the player
        if self.player_list:
            self.player_list.draw()
        # TODO: Draw other level elements as they are added

    def on_key_press(self, key, modifiers):
        """Handle key presses."""
        if key == arcade.key.ESCAPE:
            # Return to main menu
            from .start_view import StartView # Import locally to avoid circular dependency
            start_view = StartView()
            self.window.show_view(start_view)
            # start_view.setup() # Removed to fix AttributeError
        else:
            # Handle player controls via the base class and key map
            super().on_key_press(key, modifiers)
    def on_key_release(self, key, modifiers):
        """Handle key releases."""
        if key != arcade.key.ESCAPE: # Don't pass Escape to base class
             # Handle player controls via the base class and key map
            super().on_key_release(key, modifiers)


    def on_update(self, delta_time: float):
        """Update the level testing view."""
        # Update physics engines (handles player movement and collisions)
        if self.physics_engines:
            for engine in self.physics_engines:
                engine.update()

        # Update player animations and internal logic
        if self.player_list:
            for player in self.player_list:
                if hasattr(player, 'update_animation'):
                    player.update_animation(delta_time)
                if hasattr(player, 'on_update'):
                    player.on_update(delta_time)

        # --- Parallax Scrolling ---
        # Calculate the player's movement since the last update
        # Assuming player1 is the main character for camera movement
        if self.player1:
            # This is a simplified parallax. A more robust implementation
            # would involve camera movement and adjusting layer positions
            # based on the camera's change in position.
            # For this basic example, we'll just move the background
            # based on player's horizontal velocity.
            for i, sprite in enumerate(self.background_layers):
                speed = self.background_speeds[i]
                sprite.center_x += self.player1.change_x * speed * delta_time * C.CAMERA_SPEED

                # Optional: Wrap background if it goes off-screen
                # This requires careful calculation based on sprite width and screen width
                # if sprite.right < 0:
                #     sprite.left = C.SCREEN_WIDTH
                # elif sprite.left > C.SCREEN_WIDTH:
                #     sprite.right = 0