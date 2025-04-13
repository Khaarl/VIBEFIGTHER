import arcade
import arcade.gui
import math
import src.constants as C
from src.views.button_factory import TextButton, ButtonFactory
from .asset_manager import AssetManager
class StartView(arcade.View):
    """ Optimized main menu view for FHD """
    
    def __init__(self):
        super().__init__()
        self.menu_state = C.MENU_MAIN
        self.buttons = []
        self.asset_manager = AssetManager()
        self.flicker_timer = 0
        self.symbol_alpha = 0
        
        # Create title with custom font
        self.title = arcade.Text(
            "ARCADE FIGHTER",
            C.SCREEN_WIDTH/2,
            C.SCREEN_HEIGHT - 150,
            C.BONE_WHITE,
            C.FONT_SIZE_TITLE,
            anchor_x="center",
            font_name=C.FONT_PRIMARY
        )
        
        self.setup_menus()
        
    def setup_menus(self):
        """ Create buttons for all menu states """
        # Main Menu
        self.main_menu_buttons = [
            ButtonFactory.create_menu_button(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 50,
                "New Game",
                "main"
            ),
            ButtonFactory.create_menu_button(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2,
                "Options",
                "main"
            ),
            ButtonFactory.create_menu_button(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 - 50,
                "Exit",
                "main"
            )
        ]
        
        # Options Menu
        self.options_menu_buttons = [
            ButtonFactory.create_menu_button(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 100,
                "Video",
                "options"
            ),
            ButtonFactory.create_menu_button(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 50,
                "Audio",
                "options"
            ),
            ButtonFactory.create_menu_button(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2,
                "Music",
                "options"
            ),
            ButtonFactory.create_menu_button(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 - 50,
                "Back",
                "options"
            )
        ]
        
        # Video Settings Menu
        self.video_menu_buttons = [
            ButtonFactory.create_menu_button(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 150,
                "SD (800x600)",
                "video"
            ),
            ButtonFactory.create_menu_button(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 100,
                "HD (1280x720)",
                "video"
            ),
            ButtonFactory.create_menu_button(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 + 50,
                "FHD (1920x1080)",
                "video"
            ),
            ButtonFactory.create_menu_button(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2,
                "Fullscreen: ON" if C.FULLSCREEN else "Fullscreen: OFF",
                "video"
            ),
            ButtonFactory.create_menu_button(
                C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT/2 - 50,
                "Back",
                "video"
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
        if not self.asset_manager.music_player or not self.asset_manager.music_player.playing:
            self.asset_manager.play_random_music(C.MUSIC_FILES)
            
        # Resume music if returning to view
        elif self.asset_manager.music_player and not self.asset_manager.music_player.playing:
            self.asset_manager.resume_music()

    def setup_background(self):
        """ Setup static background image """
        self.background_sprites = arcade.SpriteList()
        import random
        bg_image = random.choice(C.BACKGROUND_IMAGES)
        self.background = arcade.Sprite(
            bg_image,
            center_x=C.SCREEN_WIDTH/2,
            center_y=C.SCREEN_HEIGHT/2,
            image_width=C.SCREEN_WIDTH,
            image_height=C.SCREEN_HEIGHT
        )
        self.background_sprites.append(self.background)
        
        # Optimized particle effects
        self.particles = arcade.SpriteList()
        for _ in range(30):  # Reduced from 50 to 30
            particle = arcade.SpriteCircle(
                radius=1,  # Fixed size for consistency
                color=(200, 200, 200, 150)  # Semi-transparent gray
            )
            particle.position = (
                random.randint(0, C.SCREEN_WIDTH),
                random.randint(0, C.SCREEN_HEIGHT)
            )
            particle.change_x = random.uniform(-0.1, 0.1)
            particle.change_y = random.uniform(-0.05, 0.05)
            particle.alpha = 100
            self.particles.append(particle)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        
        # Dark background base
        arcade.draw_lrbt_rectangle_filled(
            0, C.SCREEN_WIDTH, 0, C.SCREEN_HEIGHT, C.OBSIDIAN
        )
        
        # Draw background with dark overlay
        self.background_sprites.draw()
        arcade.draw_lrbt_rectangle_filled(
            0, C.SCREEN_WIDTH, 0, C.SCREEN_HEIGHT, (0, 0, 0, 180)
        )
        
        # Draw occult symbol (fading in/out)
        if self.symbol_alpha > 0:
            # Initialize symbol and sprite list if not exists
            if not hasattr(self, 'symbol'):
                self.symbol = arcade.Sprite()
                self.symbol.texture = self.asset_manager.occult_symbol
                self.symbol_list = arcade.SpriteList()
                self.symbol_list.append(self.symbol)
            
            # Update symbol properties
            self.symbol.center_x = C.SCREEN_WIDTH/2
            self.symbol.center_y = C.SCREEN_HEIGHT/2
            self.symbol.width = C.SCREEN_WIDTH * C.OCCULT_SYMBOL_SCALE
            self.symbol.height = C.SCREEN_WIDTH * C.OCCULT_SYMBOL_SCALE
            self.symbol.alpha = min(255, max(0, int(self.symbol_alpha * 2.55)))
            
            # Draw symbol via sprite list
            self.symbol_list.draw()
            
            # Add subtle vignette effect
            arcade.draw_lrbt_rectangle_filled(
                0, C.SCREEN_WIDTH, 0, C.SCREEN_HEIGHT,
                (0, 0, 0, 30)
            )
        
        # Draw particles
        self.particles.draw()
        
        # Draw title with flicker effect
        flicker = random.randint(0, 20) if self.flicker_timer <= 0 else 0
        self.title.color = (
            max(100, C.BONE_WHITE[0] - flicker),
            max(100, C.BONE_WHITE[1] - flicker),
            max(100, C.BONE_WHITE[2] - flicker)
        )
        self.title.draw()
        
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
        
        # Optimized edge wrapping
        for particle in self.particles:
            particle.center_x %= C.SCREEN_WIDTH
            particle.center_y %= C.SCREEN_HEIGHT
                
        # Update visual effects
        self.flicker_timer -= delta_time
        if self.flicker_timer <= 0:
            self.flicker_timer = C.FLICKER_INTERVAL
            
        # Smoother symbol pulse animation
        self.symbol_alpha = int(100 + 50 * math.sin(self.flicker_timer * 2))
    
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ Handle mouse movement """
        pass  # No interactive elements to handle
                
    def on_hide_view(self):
        """Called when leaving this view"""
        self.asset_manager.pause_music()