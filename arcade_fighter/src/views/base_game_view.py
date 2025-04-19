import arcade
from .. import constants as C
from ..character import Character

class BaseGameView(arcade.View):
    """Base class containing common game view setup and update logic"""

    def __init__(self):
        super().__init__()
        self.player_list: arcade.SpriteList | None = None
        self.platform_list: arcade.SpriteList | None = None
        # Store physics engines, one per player
        self.physics_engines: list[arcade.PhysicsEnginePlatformer] = []
        # Player references (populated in setup_environment)
        self.player1: Character | None = None
        # Key mapping dictionaries (populated by child views)
        # Format: {key: (player_instance, method_name, *args)}
        self.key_map_press: dict = {}
        self.key_map_release: dict = {}

    def setup_environment(self, player_count=1):
        """Common environment setup for all game views"""
        # Initialize sprite lists
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList(use_spatial_hash=True)
        self.physics_engines = [] # Reset physics engines list

        # Create platform
        platform = arcade.SpriteSolidColor(
            C.SCREEN_WIDTH, 64, arcade.color.GRAY
        )
        platform.center_x = C.SCREEN_WIDTH / 2
        platform.center_y = 32
        self.platform_list.append(platform)

        # Create players
        if player_count >= 1:
            self.player1 = Character(player_num=1, character_name="Medieval King Pack 2", scale=C.CHARACTER_SCALING)
            self.player1.center_x = C.SCREEN_WIDTH * 0.25
            self.player1.bottom = platform.top # Place on platform
            self.player_list.append(self.player1)


        # Setup physics engine for player 1
        if self.player1:
            engine = arcade.PhysicsEnginePlatformer(
                self.player1,
                self.platform_list,
                gravity_constant=C.GRAVITY
            )
            self.physics_engines.append(engine)

    def on_update(self, delta_time: float):
        """ Base update logic for physics and players """
        # Update physics engines
        if self.physics_engines:
            for engine in self.physics_engines:
                engine.update()

        # Update player animations and internal logic
        # Assuming Character class has on_update method
        if self.player_list:
            for player in self.player_list:
                if hasattr(player, 'update_animation'):
                    player.update_animation(delta_time)
                if hasattr(player, 'on_update'):
                    player.on_update(delta_time)

    # --- Generic Key Handling ---
    def on_key_press(self, key, modifiers):
        """Handles key presses based on the key_map_press."""
        if key in self.key_map_press:
            player, method_name, args = self.key_map_press[key]
            if player and hasattr(player, method_name):
                try:
                    method = getattr(player, method_name)
                    method(*args)
                except AttributeError as e:
                    print(f"Error calling method {method_name} on {player}: {e}")
                except TypeError as e:
                    print(f"Error calling method {method_name} with args {args}: {e}")
            elif C.DEBUG_MODE:
                 print(f"Warning: Player not found or method '{method_name}' not in {player} for key {key}")


    def on_key_release(self, key, modifiers):
        """Handles key releases based on the key_map_release."""
        if key in self.key_map_release:
            player, method_name, args = self.key_map_release[key]
            if player and hasattr(player, method_name):
                try:
                    method = getattr(player, method_name)
                    method(*args)
                except AttributeError as e:
                    print(f"Error calling method {method_name} on {player}: {e}")
                except TypeError as e:
                    print(f"Error calling method {method_name} with args {args}: {e}")
            elif C.DEBUG_MODE:
                print(f"Warning: Player not found or method '{method_name}' not in {player} for key {key}")

    def on_draw(self):
        """Common drawing logic for game views."""
        self.clear()
        if self.platform_list:
            self.platform_list.draw()
        if self.player_list:
            self.player_list.draw()