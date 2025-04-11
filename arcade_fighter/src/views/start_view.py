import arcade
from .. import constants as C

class StartView(arcade.View):
    """ View to show before the game starts """

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        self.window.viewport = (0, 0, C.SCREEN_WIDTH, C.SCREEN_HEIGHT)

    def on_draw(self):
        """ Draw this view """
        self.clear()
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