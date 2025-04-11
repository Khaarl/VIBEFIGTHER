import arcade
import os
from typing import Optional

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
from .. import constants as C

class StartView(arcade.View):
    """ View to show before the game starts """

    def generate_fractal(self, x1, y1, x2, y2, x3, y3, depth):
        """ Recursively draw a Sierpinski triangle """
        if depth == 0:
            arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, arcade.color.DARK_BLUE_GRAY)
            return
        
        # Calculate midpoints
        x12 = (x1 + x2) / 2
        y12 = (y1 + y2) / 2
        x13 = (x1 + x3) / 2
        y13 = (y1 + y3) / 2
        x23 = (x2 + x3) / 2
        y23 = (y2 + y3) / 2
        
        # Recursively draw smaller triangles
        self.generate_fractal(x1, y1, x12, y12, x13, y13, depth - 1)
        self.generate_fractal(x12, y12, x2, y2, x23, y23, depth - 1)
        self.generate_fractal(x13, y13, x23, y23, x3, y3, depth - 1)
    def on_show_view(self):
        """ This is run once when we switch to this view """
        # Background color removed to use fractal background
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        self.window.viewport = (0, 0, C.SCREEN_WIDTH, C.SCREEN_HEIGHT)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        # Draw fractal background
        self.generate_fractal(0, 0, C.SCREEN_WIDTH, 0, C.SCREEN_WIDTH/2, C.SCREEN_HEIGHT, 5)
        arcade.draw_text("ARCADE FIGHTER", C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT / 2 + 50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Press ENTER to Start", C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """ If the user presses the Enter key, start the game. """
        if key == arcade.key.ENTER:
            print("Starting GameView...") # Debug print
            # We will create GameView later, for now, this import might fail
            # until game_view.py exists.
            try:
                from .game_view import GameView # Import here to avoid circular import
                game_view = GameView()
                game_view.setup()
                self.window.show_view(game_view)
            except NameError:
                 print("GameView not yet defined/imported properly.")
            except AttributeError:
                 print("GameView might exist but missing setup() method.")