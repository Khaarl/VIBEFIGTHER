import arcade
import argparse
import src.constants as C
from src.views.start_view import StartView
from src.views.debug_game_view import DebugGameView

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--test", action="store_true", help="Start in test mode")
    return parser.parse_args()

def main():
    """ Main function """
    args = parse_args()
    
    # Set debug mode if flag is present
    if args.debug:
        C.DEBUG_MODE = True
    
    window = arcade.Window(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.SCREEN_TITLE)
    
    # Start in debug view if debug flag is set
    if args.debug:
        debug_view = DebugGameView()
        debug_view.setup()
        window.show_view(debug_view)
    else:
        start_view = StartView()
        window.show_view(start_view)
        
    arcade.run()

if __name__ == "__main__":
    main()