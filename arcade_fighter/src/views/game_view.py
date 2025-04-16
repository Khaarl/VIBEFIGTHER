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

        # Physics engines are now set up in BaseGameView.setup_environment

        # Initialize UI
        self._init_ui_elements()

        # --- Setup Key Mappings ---
        # Ensure players exist before mapping keys
        if self.player1:
            self.key_map_press[C.KEY_LEFT_P1] = (self.player1, 'move', (-1,))
            self.key_map_press[C.KEY_RIGHT_P1] = (self.player1, 'move', (1,))
            self.key_map_press[C.KEY_JUMP_P1] = (self.player1, 'jump', ())
            # Add attack key if defined
            if hasattr(C, 'KEY_ATTACK_P1'):
                 self.key_map_press[C.KEY_ATTACK_P1] = (self.player1, 'attack', ())

            self.key_map_release[C.KEY_LEFT_P1] = (self.player1, 'stop_moving', ())
            self.key_map_release[C.KEY_RIGHT_P1] = (self.player1, 'stop_moving', ())

        if self.player2:
            self.key_map_press[C.KEY_LEFT_P2] = (self.player2, 'move', (-1,))
            self.key_map_press[C.KEY_RIGHT_P2] = (self.player2, 'move', (1,))
            self.key_map_press[C.KEY_JUMP_P2] = (self.player2, 'jump', ())
            # Add attack key if defined
            if hasattr(C, 'KEY_ATTACK_P2'):
                 self.key_map_press[C.KEY_ATTACK_P2] = (self.player2, 'attack', ())

            self.key_map_release[C.KEY_LEFT_P2] = (self.player2, 'stop_moving', ())
            self.key_map_release[C.KEY_RIGHT_P2] = (self.player2, 'stop_moving', ())


    def on_key_press(self, key, modifiers):
        """Handle key press events with debug logging"""
        # Debug toggle
        if key == C.KEY_TOGGLE_DEBUG:
            C.DEBUG_MODE = not C.DEBUG_MODE
            print(f"\nDEBUG MODE {'ENABLED' if C.DEBUG_MODE else 'DISABLED'}\n")
            return
            
        # Handle player controls via the base class and key map
        super().on_key_press(key, modifiers)

        # Keep debug logging if needed
        if C.DEBUG_MODE:
            print(f"Key PRESSED: {key} (modifiers: {modifiers})")
            
    def on_key_release(self, key, modifiers):
        """Handle key release events with debug logging"""
        # Handle player controls via the base class and key map
        super().on_key_release(key, modifiers)

        # Keep debug logging if needed
        if C.DEBUG_MODE:
            print(f"Key RELEASED: {key}")
    def on_update(self, delta_time: float):
        """ Update game state, physics, and animations """
        # Call base class update logic (handles physics, player animations, player logic)
        super().on_update(delta_time)

        # TODO: Add game logic updates (collision checks, scoring, round end, etc.)

    # Rest of the class implementation remains unchanged...
