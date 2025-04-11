import arcade
import os
import random
import math
from typing import Optional
from .. import constants as C

class TextButton:
    """ Text-based button for menu """
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 width: float,
                 height: float,
                 text: str,
                 font_size: int = 18,
                 font_color = arcade.color.WHITE,  # type: ignore[attr-defined]
                 face_color = arcade.color.DARK_BLUE_GRAY,  # type: ignore[attr-defined]
                 highlight_color = arcade.color.LIGHT_BLUE,  # type: ignore[attr-defined]
                 shadow_color = arcade.color.BLACK,  # type: ignore[attr-defined]
                 button_height: int = 2):
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

    def draw(self):
        """ Draw the button """
        arcade.draw_rectangle_filled(
            self.center_x, self.center_y, self.width,
            self.height, self.face_color)

        if not self.pressed:
            arcade.draw_rectangle_filled(
                self.center_x, self.center_y + self.button_height/2,
                self.width, self.button_height, self.shadow_color)

        arcade.draw_text(
            self.text, self.center_x, self.center_y,
            self.font_color, self.font_size,
            align="center", anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

    def check_mouse_press(self, x, y):
        if (x > self.center_x - self.width/2 and
            x < self.center_x + self.width/2 and
            y > self.center_y - self.height/2 and
            y < self.center_y + self.height/2):
            self.on_press()
            return True
        return False

    def check_mouse_release(self, x, y):
        if self.pressed:
            self.on_release()
            return (x > self.center_x - self.width/2 and
                    x < self.center_x + self.width/2 and
                    y > self.center_y - self.height/2 and
                    y < self.center_y + self.height/2)
        return False

class StartView(arcade.View):
    """ View to show before the game starts with enhanced background """

    def setup_background(self):
        """ Setup dynamic background elements """
        # Particle system for animated stars
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
            
        # Parallax layers using sprites
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

    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.setup_background()
        self.window.viewport = (0, 0, C.SCREEN_WIDTH, C.SCREEN_HEIGHT)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        
        # Draw dark gradient background using sprite list
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
        
        # Draw parallax layers
        for layer in self.parallax_layers:
            layer.draw()
            
        # Draw particles through sprite list
        self.particles.draw()
        
        # Draw interactive elements with glow effect
        for sprite in self.interactive_sprites:
            arcade.draw_circle_filled(
                sprite.center_x, sprite.center_y,
                sprite.width * 1.5,
                (255, 215, 0, 50)  # Gold with transparency
            )
        self.interactive_sprites.draw()
        
        # Draw menu text with shadow for better visibility
        arcade.draw_text("ARCADE FIGHTER", C.SCREEN_WIDTH / 2 + 2, C.SCREEN_HEIGHT / 2 + 48,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("ARCADE FIGHTER", C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT / 2 + 50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        
        arcade.draw_text("Press ENTER to Start", C.SCREEN_WIDTH / 2 + 1, C.SCREEN_HEIGHT / 2 - 51,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Press ENTER to Start", C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

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

    def on_key_press(self, key, modifiers):
        """ If the user presses the Enter key, start the game. """
        if key == arcade.key.ENTER:
            print("Starting GameView...")
            try:
                from .game_view import GameView
                game_view = GameView()
                game_view.setup()
                self.window.show_view(game_view)
            except NameError:
                 print("GameView not yet defined/imported properly.")
            except AttributeError:
                 print("GameView might exist but missing setup() method.")