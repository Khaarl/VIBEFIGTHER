import arcade
from .. import constants as C
from ..character import Character

class BaseGameView(arcade.View):
    """Base class containing common game view setup code"""
    
    def __init__(self):
        super().__init__()
        self.player_list = None
        self.platform_list = None
        self.physics_engine = None
        
    def setup_environment(self, player_count=1):
        """Common environment setup for all game views"""
        # Initialize sprite lists
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList(use_spatial_hash=True)
        
        # Create platform
        platform = arcade.SpriteSolidColor(
            C.SCREEN_WIDTH, 64, arcade.color.GRAY
        )
        platform.center_x = C.SCREEN_WIDTH / 2
        platform.center_y = 32
        self.platform_list.append(platform)
        
        # Create players
        if player_count >= 1:
            self.player1 = Character(player_num=1, scale=C.CHARACTER_SCALING)
            self.player1.center_x = C.SCREEN_WIDTH * 0.25
            self.player1.bottom = 64
            self.player_list.append(self.player1)
            
        if player_count >= 2:
            self.player2 = Character(player_num=2, scale=C.CHARACTER_SCALING)
            self.player2.center_x = C.SCREEN_WIDTH * 0.75
            self.player2.bottom = 64
            self.player_list.append(self.player2)
            
        # Setup physics
        if hasattr(self, 'player1'):
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player1,
                self.platform_list,
                gravity_constant=C.GRAVITY
            )