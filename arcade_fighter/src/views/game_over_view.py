import arcade
from .. import constants as C

class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self, winner=None):
        """ This is run once when we switch to this view"""
        super().__init__()
        self.winner = winner # Store who won

        # Reset the viewport, necessary if scaling was used in the game view
        self.window.viewport = (0, 0, C.SCREEN_WIDTH, C.SCREEN_HEIGHT)

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw this view """
        self.clear()

        # Display winner information
        winner_text = f"Player {self.winner} Wins!" if self.winner else "Game Over!"
        arcade.draw_text(winner_text, C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT / 2 + 50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        arcade.draw_text("Press ENTER to Play Again", C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press ESCAPE to Quit", C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT / 2 - 100,
                         arcade.color.WHITE, font_size=18, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """ If the user presses the Enter key, restart the game. """
        if key == arcade.key.ENTER:
            print("Restarting game...") # Debug print
            # We need to import GameView here or pass it somehow if we want
            # to directly go back to game. Going to StartView is simpler.
            from .start_view import StartView # Import here
            start_view = StartView()
            self.window.show_view(start_view)
        elif key == arcade.key.ESCAPE:
            print("Quitting game...") # Debug print
            arcade.exit()