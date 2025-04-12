import arcade
import os
import random
import math
from typing import Optional
from .. import constants as C

class TextButton:
    """ Complete text button implementation """
    def __init__(self, center_x, center_y, width, height, text, font_size=18,
                font_color=arcade.color.WHITE, face_color=arcade.color.DARK_BLUE_GRAY,
                highlight_color=arcade.color.LIGHT_BLUE, shadow_color=arcade.color.BLACK,
                button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height
        self.pressed = False
        self._text_obj = None
        self.create_text()

    def create_text(self):
        """ Create cached text object """
        self._text_obj = arcade.Text(
            self.text, self.center_x, self.center_y,
            self.font_color, self.font_size,
            align="center", anchor_x="center", anchor_y="center"
        )

    def draw(self):
        """ Draw the button """
        arcade.draw_lrbt_rectangle_filled(
            self.center_x - self.width/2, self.center_x + self.width/2,
            self.center_y - self.height/2, self.center_y + self.height/2,
            self.face_color)

        if not self.pressed:
            arcade.draw_lrbt_rectangle_filled(
                self.center_x - self.width/2, self.center_x + self.width/2,
                self.center_y, self.center_y + self.button_height,
                self.shadow_color)

        self._text_obj.draw()

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

    def check_mouse_press(self, x, y):
        """ Check if mouse click is within button bounds """
        if (x > self.center_x - self.width/2 and
            x < self.center_x + self.width/2 and
            y > self.center_y - self.height/2 and
            y < self.center_y + self.height/2):
            self.on_press()
            return True
        return False

    def check_mouse_release(self, x, y):
        """ Check if mouse release is within button bounds """
        if self.pressed:
            self.on_release()
            return (x > self.center_x - self.width/2 and
                    x < self.center_x + self.width/2 and
                    y > self.center_y - self.height/2 and
                    y < self.center_y + self.height/2)
        return False

class StartView(arcade.View):
    """ Optimized main menu view for FHD """
    
    def __init__(self):
        super().__init__()
        self.menu_state = C.MENU_MAIN
        self.buttons = []
        self.music_player = None
        self.current_volume = C.DEFAULT_VOLUME
        self.current_track = None
        self.title_text = arcade.Text(
            "ARCADE FIGHTER", C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT - 100,
            C.WHITE, font_size=50, anchor_x="center"
        )
        self.setup_menus()
        
    def setup_menus(self):
        """ Create buttons for all menu states """
        # Main Menu
        self.main_menu_buttons = [
            TextButton(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 50,
                C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                "New Game",
                font_size=24
            ),
            TextButton(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2,
                C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                "Options",
                font_size=24
            ),
            TextButton(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 - 50,
                C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                "Exit",
                font_size=24
            )
        ]
        
        # Options Menu
        self.options_menu_buttons = [
            TextButton(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 100,
                C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                "Video",
                font_size=24
            ),
            TextButton(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 50,
                C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                "Audio",
                font_size=24
            ),
            TextButton(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2,
                C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                "Music",
                font_size=24
            ),
            TextButton(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 - 50,
                C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                "Back",
                font_size=24
            )
        ]
        
        # Video Settings Menu
        self.video_menu_buttons = [
            TextButton(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 150,
                C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                "SD (800x600)",
                font_size=24
            ),
            TextButton(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 100,
                C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                "HD (1280x720)",
                font_size=24
            ),
            TextButton(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 50,
                C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                "FHD (1920x1080)",
                font_size=24
            ),
            TextButton(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2,
                C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                "Fullscreen: ON" if C.FULLSCREEN else "Fullscreen: OFF",
                font_size=24
            ),
            TextButton(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 - 50,
                C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                "Back",
                font_size=24
            )
        ]

    def create_debug_button(self):
        """Create debug mode toggle button"""
        debug_button = arcade.gui.UIFlatButton(
            text="Debug Mode: OFF" if not C.DEBUG_MODE else "Debug Mode: ON",
            width=200,
            height=40,
            style={
                "font_size": 14,
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.RED if C.DEBUG_MODE else arcade.color.DARK_GREEN
            }
        )
        debug_button.on_click = self.on_click_debug
        return debug_button
        
    def on_click_debug(self, event):
        """Toggle debug mode"""
        C.DEBUG_MODE = not C.DEBUG_MODE
        self.manager.clear()
        self.setup()
        
    def on_show_view(self):
        """ Called when switching to this view """
        self.setup_background()
        self.window.set_fullscreen(C.FULLSCREEN)
        self.menu_state = C.MENU_MAIN
        
        # Start random music if not already playing
        if not self.music_player or not self.music_player.playing:
            self.play_random_music()
            
        # Resume music if returning to view
        elif self.music_player and not self.music_player.playing:
            self.music_player.play()

    def setup_background(self):
        """ Setup dynamic background elements """
        # Particle system
        self.particles = arcade.SpriteList()
        for _ in range(100):
            particle = arcade.SpriteCircle(
                radius=random.randint(1, 3),
                color=random.choice([
                    arcade.color.WHITE,
                    arcade.color.LIGHT_BLUE,
                    arcade.color.LIGHT_STEEL_BLUE
                ])
            )
            particle.position = (
                random.randint(0, C.SCREEN_WIDTH),
                random.randint(0, C.SCREEN_HEIGHT)
            )
            particle.change_x = random.uniform(-0.2, 0.2)
            particle.change_y = random.uniform(-0.1, 0.1)
            self.particles.append(particle)
            
        # Parallax layers
        self.parallax_layers = []
        for i in range(3):
            layer = arcade.SpriteList()
            for _ in range(20):
                sprite = arcade.SpriteSolidColor(
                    width=(i+1)*2, 
                    height=(i+1)*2,
                    color=arcade.color.GRAY if i == 0 else 
                          arcade.color.DARK_GRAY if i == 1 else
                          arcade.color.DARK_SLATE_GRAY
                )
                sprite.position = (
                    random.randint(0, C.SCREEN_WIDTH),
                    random.randint(0, C.SCREEN_HEIGHT)
                )
                layer.append(sprite)
            self.parallax_layers.append(layer)
            
        # Interactive elements
        self.interactive_sprites = arcade.SpriteList()
        for _ in range(5):
            sprite = arcade.SpriteCircle(
                radius=10,
                color=arcade.color.GOLD
            )
            sprite.position = (
                random.randint(50, C.SCREEN_WIDTH-50),
                random.randint(50, C.SCREEN_HEIGHT-50)
            )
            self.interactive_sprites.append(sprite)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        
        # Draw background
        if not hasattr(self, 'background_sprites'):
            self.background_sprites = arcade.SpriteList()
            background = arcade.Sprite(
                ":resources:images/backgrounds/stars.png",
                center_x=C.SCREEN_WIDTH/2,
                center_y=C.SCREEN_HEIGHT/2,
                image_width=C.SCREEN_WIDTH,
                image_height=C.SCREEN_HEIGHT
            )
            self.background_sprites.append(background)
        self.background_sprites.draw()
        
        # Draw effects
        for layer in self.parallax_layers:
            layer.draw()
        self.particles.draw()
        
        # Draw interactive elements
        for sprite in self.interactive_sprites:
            arcade.draw_circle_filled(
                sprite.center_x, sprite.center_y,
                sprite.width * 1.5,
                (255, 215, 0, 50)
            )
        self.interactive_sprites.draw()
        
        # Draw UI
        self.title_text.draw()
        
        # Draw current menu buttons
        if self.menu_state == C.MENU_MAIN:
            for button in self.main_menu_buttons:
                button.draw()
        elif self.menu_state == C.MENU_OPTIONS:
            for button in self.options_menu_buttons:
                button.draw()
        elif self.menu_state == C.MENU_VIDEO:
            for button in self.video_menu_buttons:
                button.draw()
        elif self.menu_state == "mode_select":
            for button in self.mode_select_buttons:
                button.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """ Handle mouse clicks """
        if self.menu_state == C.MENU_MAIN:
            for btn in self.main_menu_buttons:
                if btn.check_mouse_press(x, y):
                    if btn.text == "New Game":
                        self.show_game_mode_selection()
                    elif btn.text == "Options":
                        self.menu_state = C.MENU_OPTIONS
                    elif btn.text == "Exit":
                        arcade.exit()
        
        elif self.menu_state == "mode_select":
            for btn in self.mode_select_buttons:
                if btn.check_mouse_press(x, y):
                    if btn.text == "Standard Mode":
                        self.start_game(debug_mode=False)
                    elif btn.text == "Debug Mode":
                        self.start_game(debug_mode=True)
                    elif btn.text == "Back":
                        self.menu_state = C.MENU_MAIN
        
        elif self.menu_state == C.MENU_OPTIONS:
            for btn in self.options_menu_buttons:
                if btn.check_mouse_press(x, y):
                    if btn.text == "Video":
                        self.menu_state = C.MENU_VIDEO
                    elif btn.text == "Back":
                        self.menu_state = C.MENU_MAIN
        
        elif self.menu_state == C.MENU_VIDEO:
            for btn in self.video_menu_buttons:
                if btn.check_mouse_press(x, y):
                    if btn.text.startswith("SD"):
                        self.set_resolution("SD")
                    elif btn.text.startswith("HD"):
                        self.set_resolution("HD")
                    elif btn.text.startswith("FHD"):
                        self.set_resolution("FHD")
                    elif btn.text.startswith("Fullscreen"):
                        self.toggle_fullscreen()
                    elif btn.text == "Back":
                        self.menu_state = C.MENU_OPTIONS

    def on_key_press(self, key, modifiers):
        """ Handle keyboard input """
        if key == arcade.key.ENTER and self.menu_state == C.MENU_MAIN:
            self.start_game()
        elif key == arcade.key.ESCAPE:
            if self.menu_state == C.MENU_OPTIONS:
                self.menu_state = C.MENU_MAIN
            elif self.menu_state == C.MENU_VIDEO:
                self.menu_state = C.MENU_OPTIONS

    def toggle_fullscreen(self):
        """ Toggle fullscreen mode """
        C.FULLSCREEN = not C.FULLSCREEN
        self.window.set_fullscreen(C.FULLSCREEN)
        
        # Update fullscreen button text
        for button in self.video_menu_buttons:
            if button.text.startswith("Fullscreen"):
                button.text = "Fullscreen: ON" if C.FULLSCREEN else "Fullscreen: OFF"
                break

    def set_resolution(self, res_key):
        """ Change screen resolution and update all dependent values """
        was_fullscreen = C.FULLSCREEN
        if was_fullscreen:
            self.window.set_fullscreen(False)
            
        # Update resolution constants
        C.set_resolution(res_key)
        
        # Apply window size changes
        self.window.set_size(C.SCREEN_WIDTH, C.SCREEN_HEIGHT)
        
        if was_fullscreen:
            self.window.set_fullscreen(True)
            
        # Update all UI elements
        self.setup_menus()
        self.setup_background()

    def show_game_mode_selection(self):
        """Show game mode selection buttons"""
        self.menu_state = "mode_select"
        
        # Create mode selection buttons if they don't exist
        if not hasattr(self, 'mode_select_buttons'):
            self.mode_select_buttons = [
                TextButton(
                    C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 50,
                    C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                    "Standard Mode",
                    font_size=24,
                    face_color=arcade.color.DARK_GREEN
                ),
                TextButton(
                    C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2,
                    C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                    "Debug Mode",
                    font_size=24,
                    face_color=arcade.color.DARK_RED
                ),
                TextButton(
                    C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 - 50,
                    C.BUTTON_WIDTH, C.BUTTON_HEIGHT,
                    "Back",
                    font_size=24
                )
            ]
    
    def start_game(self, debug_mode=False):
        """ Start the game """
        print("Starting GameView...")
        C.DEBUG_MODE = debug_mode
        from src.views.game_view import GameView
        game_view = GameView()
        self.window.show_view(game_view)
        game_view.setup()

    def on_update(self, delta_time: float):
        """ Animate background elements """
        # Update particles
        self.particles.update()
        
        # Wrap particles around screen edges
        for particle in self.particles:
            if particle.center_x < 0:
                particle.center_x = C.SCREEN_WIDTH
            elif particle.center_x > C.SCREEN_WIDTH:
                particle.center_x = 0
            if particle.center_y < 0:
                particle.center_y = C.SCREEN_HEIGHT
            elif particle.center_y > C.SCREEN_HEIGHT:
                particle.center_y = 0
                
        # Animate parallax layers
        for i, layer in enumerate(self.parallax_layers):
            for sprite in layer:
                sprite.center_x -= (i+1) * 0.1
                if sprite.center_x < -10:
                    sprite.center_x = C.SCREEN_WIDTH + 10
    
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ Make interactive elements respond to mouse """
        for sprite in self.interactive_sprites:
            dist = math.sqrt((x - sprite.center_x)**2 + (y - sprite.center_y)**2)
            if dist < 100:
                sprite.center_x += dx * 0.3
                sprite.center_y += dy * 0.3
                
    def play_random_music(self):
        """Play a randomly selected music track"""
        import random
        if self.music_player:
            self.music_player.stop()
            
        self.current_track = random.choice(C.MUSIC_FILES)
        sound = arcade.load_sound(self.current_track)
        self.music_player = sound.play(volume=self.current_volume)
        self.music_player.loop = True
        
    def adjust_volume(self, change: float):
        """Adjust volume by specified amount (clamped to 0-1)"""
        self.current_volume = max(0, min(1, self.current_volume + change))
        if self.music_player:
            self.music_player.volume = self.current_volume
            
    def on_hide_view(self):
        """Called when leaving this view"""
        if self.music_player:
            self.music_player.pause()