import arcade
import src.constants as C
from src.views.start_view import StartView
# GameView and GameOverView are imported by StartView/GameView as needed

def main():
    """ Main function """
    window = arcade.Window(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()