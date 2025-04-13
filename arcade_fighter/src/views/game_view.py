import arcade
from arcade import Text
from .. import constants as C
from ..character import Character
from .game_over_view import GameOverView

class GameView(arcade.View):
    """Main application class where the fighting happens."""

    def __init__(self):
        """Initializer"""
        # Call the parent class initializer
        super().__init__()

        # Initialize variables with None
        self.player_list = None
        self.platform_list = None
        self.player1_sprite = None
        self.player2_sprite = None
        self.physics_engine_p1 = None
        self.physics_engine_p2 = None
        self.player1_text = None
        self.player2_text = None
        self.round_text = None
        self.placeholder_text = None
        self.debug_texts = []

    def setup(self):
        """Set up the game with initial state"""
        # Initialize sprite lists
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList(use_spatial_hash=True)

        # Set background color
        arcade.set_background_color(C.BACKGROUND_COLOR)

        # Initialize game state
        self.round_number = 1
        self.player1_rounds_won = 0
        self.player2_rounds_won = 0

        # Player setup
        self.player1_sprite = Character(player_num=1, scale=C.CHARACTER_SCALING)
        self.player1_sprite.center_x = C.SCREEN_WIDTH * 0.25
        self.player1_sprite.bottom = 64
        self.player_list.append(self.player1_sprite)

        self.player2_sprite = Character(player_num=2, scale=C.CHARACTER_SCALING)
        self.player2_sprite.center_x = C.SCREEN_WIDTH * 0.75
        self.player2_sprite.bottom = 64
        self.player_list.append(self.player2_sprite)

        # Floor setup
        floor = arcade.SpriteSolidColor(
            int(C.SCREEN_WIDTH * 1.5), 
            64, 
            arcade.color.DARK_SPRING_GREEN
        )
        floor.center_x = C.SCREEN_WIDTH / 2
        floor.center_y = 32
        self.platform_list.append(floor)

        # Physics engine setup
        if self.player1_sprite:
            self.physics_engine_p1 = arcade.PhysicsEnginePlatformer(
                self.player1_sprite, 
                self.platform_list, 
                gravity_constant=C.GRAVITY
            )
        if self.player2_sprite:
            self.physics_engine_p2 = arcade.PhysicsEnginePlatformer(
                self.player2_sprite, 
                self.platform_list, 
                gravity_constant=C.GRAVITY
            )

        # Initialize UI
        self._init_ui_elements()

    # Rest of the class implementation remains unchanged...
