import arcade
from ..character import Character
from .. import constants as C

class DebugGameView(arcade.View):
    """Simplified view for animation testing"""
    
    def __init__(self):
        super().__init__()
        self.player = None
        self.platform = None
        self.keys_pressed = set()
        
    def setup(self):
        """Set up the testing environment"""
        # Simple black background
        arcade.set_background_color(arcade.color.BLACK)
        
        # Create player list and add player
        self.player_list = arcade.SpriteList()
        self.player = Character(player_num=1, scale=C.CHARACTER_SCALING)
        self.player.center_x = C.SCREEN_WIDTH / 2
        self.player.bottom = 64
        self.player_list.append(self.player)
        
        # Simple gray platform in sprite list
        self.platform_list = arcade.SpriteList()
        platform = arcade.SpriteSolidColor(
            C.SCREEN_WIDTH, 64, arcade.color.GRAY
        )
        platform.center_x = C.SCREEN_WIDTH / 2
        platform.center_y = 32
        self.platform_list.append(platform)
        
    def on_draw(self):
        """Render the screen"""
        self.clear()
        self.platform_list.draw()
        self.player_list.draw()
        
    def on_key_press(self, key, modifiers):
        """Handle key presses for animation testing"""
        self.keys_pressed.add(key)
        
        if key == arcade.key.LEFT:
            self.player.change_x = -C.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = C.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            self.player.attack()
        elif key == arcade.key.UP:
            self.player.jump()
            
    def on_key_release(self, key, modifiers):
        """Handle key releases"""
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
            
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0
            
    def update(self, delta_time):
        """Game logic updates"""
        self.player.update_animation(delta_time)
        self.player.update()