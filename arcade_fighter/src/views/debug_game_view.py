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
        
        # Initialize fresh sprite lists
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList(use_spatial_hash=True)
        
        # Create and position new player instance
        self.player = Character(player_num=1, scale=C.CHARACTER_SCALING)
        self.player.center_x = C.SCREEN_WIDTH / 2
        self.player.bottom = 64
        self.player_list.append(self.player)
        
        # Create platform
        platform = arcade.SpriteSolidColor(
            C.SCREEN_WIDTH, 64, arcade.color.GRAY
        )
        platform.center_x = C.SCREEN_WIDTH / 2
        platform.center_y = 32
        self.platform_list.append(platform)
        
        # Setup physics engine with debug logging
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.platform_list,
            gravity_constant=C.GRAVITY
        )
        
        if C.DEBUG_MODE:
            print("DebugGameView setup complete")
            print(f"Player position: ({self.player.center_x}, {self.player.center_y})")
        
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
        if not hasattr(self, 'player') or self.player is None:
            return
            
        self.keys_pressed.add(key)
        
        try:
            if key == arcade.key.LEFT:
                self.player.change_x = -C.PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.player.change_x = C.PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.SPACE:
                self.player.attack()
            elif key == arcade.key.UP:
                self.player.jump()
        except AttributeError as e:
            print(f"Debug: Key press error - {str(e)}")
            
    def on_key_release(self, key, modifiers):
        """Handle key releases"""
        if not hasattr(self, 'player') or self.player is None:
            return
            
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
            
        try:
            if key in (arcade.key.LEFT, arcade.key.RIGHT):
                self.player.change_x = 0
        except AttributeError as e:
            print(f"Debug: Key release error - {str(e)}")
            
    def update(self, delta_time):
        """Game logic updates"""
        if not hasattr(self, 'player') or self.player is None:
            return
            
        # Update physics first
        self.physics_engine.update()
        
        # Update player state based on movement
        if abs(self.player.change_x) > 0:
            if self.physics_engine.can_jump():
                self.player.state = C.STATE_WALKING
        elif self.physics_engine.can_jump():
            self.player.state = C.STATE_IDLE
            
        # Airborne state
        if not self.physics_engine.can_jump():
            if self.player.change_y > 0:
                self.player.state = C.STATE_JUMPING
            else:
                self.player.state = C.STATE_FALLING
                
        # Update animations
        self.player.update_animation(delta_time)
        self.player.update()
        
        # Detailed debug logging
        if C.DEBUG_MODE:
            print(f"\n--- Frame Update ---")
            print(f"State: {self.player.state}")
            print(f"Position: ({self.player.center_x:.1f}, {self.player.center_y:.1f})")
            print(f"Velocity: (X:{self.player.change_x:.1f}, Y:{self.player.change_y:.1f})")
            print(f"On ground: {self.physics_engine.can_jump()}")
            print(f"Keys pressed: {self.keys_pressed}")
            
            # Physics debug info
            if hasattr(self.player, 'is_on_ground'):
                print(f"Ground state: {self.player.is_on_ground}")
            
            # Collision checks
            if hasattr(self.physics_engine, 'check_for_collision'):
                collisions = self.physics_engine.check_for_collision()
                if collisions:
                    print(f"Collisions: {len(collisions)}")
                    for i, collision in enumerate(collisions[:3], 1):
                        print(f"  Collision {i}: {collision}")
            
            # State transition info
            if hasattr(self.player, 'previous_state'):
                if self.player.previous_state != self.player.state:
                    print(f"State changed from {self.player.previous_state} to {self.player.state}")