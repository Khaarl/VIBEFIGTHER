import arcade
from arcade import Text
from .base_game_view import BaseGameView
from .game_over_view import GameOverView
from .. import constants as C

class GameView(BaseGameView):
    """Main application class where the fighting happens."""

    def __init__(self):
        """Initializer"""
        super().__init__()
        self.player1_text = None
        self.player2_text = None
        self.round_text = None
        self.placeholder_text = None
        self.debug_texts = []
        self.physics_engine_p1 = None
        self.physics_engine_p2 = None

    def setup(self):
        """Set up the game with initial state"""
        # Setup common environment
        super().setup_environment(player_count=2)
        
        # Set background color
        arcade.set_background_color(C.BACKGROUND_COLOR)

        # Initialize game state
        self.round_number = 1
        self.player1_rounds_won = 0
        self.player2_rounds_won = 0

        # Setup physics engines for both players
        # Add small padding (2 pixels) to make ground detection more lenient
        self.physics_engine_p1 = arcade.PhysicsEnginePlatformer(
            self.player1,
            self.platform_list,
            gravity_constant=C.GRAVITY,
            platforms_padding=2
        )
        self.physics_engine_p2 = arcade.PhysicsEnginePlatformer(
            self.player2,
            self.platform_list,
            gravity_constant=C.GRAVITY,
            platforms_padding=2
        )

        # Initialize UI
        self._init_ui_elements()


    def on_key_press(self, key, modifiers):
        """Handle key press events with debug logging"""
        # Debug toggle
        if key == C.KEY_TOGGLE_DEBUG:
            C.DEBUG_MODE = not C.DEBUG_MODE
            print(f"\nDEBUG MODE {'ENABLED' if C.DEBUG_MODE else 'DISABLED'}\n")
            return
            
        if C.DEBUG_MODE:
            print(f"Key PRESSED: {key} (modifiers: {modifiers})")
            
        # Player 1 controls
        if key == C.KEY_LEFT_P1:
            self.player1_sprite.move(-1)
        elif key == C.KEY_RIGHT_P1:
            self.player1_sprite.move(1)
        elif key == C.KEY_JUMP_P1:
            self.player1_sprite.jump()
            
        # Player 2 controls
        elif key == C.KEY_LEFT_P2:
            self.player2_sprite.move(-1)
        elif key == C.KEY_RIGHT_P2:
            self.player2_sprite.move(1)
        elif key == C.KEY_JUMP_P2:
            self.player2_sprite.jump()
            
    def on_key_release(self, key, modifiers):
        """Handle key release events with debug logging"""
        if C.DEBUG_MODE:
            print(f"Key RELEASED: {key}")
            
        # Player 1 controls
        if key in (C.KEY_LEFT_P1, C.KEY_RIGHT_P1):
            self.player1_sprite.stop_moving()
            
        # Player 2 controls
        elif key in (C.KEY_LEFT_P2, C.KEY_RIGHT_P2):
            self.player2_sprite.stop_moving()
    def on_update(self, delta_time: float):
        """ Update game state, physics, and animations """
        # Update physics engines
        self.physics_engine_p1.update()
        self.physics_engine_p2.update()

        # Update character animations
        # Note: Character.update_animation currently has issues (walking, attack, etc.)
        self.player1_sprite.update_animation(delta_time)
        self.player2_sprite.update_animation(delta_time)

        # Update character internal logic (timers, etc.)
        self.player1_sprite.on_update(delta_time)
        self.player2_sprite.on_update(delta_time)

        # TODO: Add game logic updates (collision checks, scoring, round end, etc.)

    # Rest of the class implementation remains unchanged...
