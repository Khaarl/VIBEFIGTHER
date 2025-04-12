import unittest
import arcade
from src.views.game_view import GameView
from src import constants as C

class TestGameView(unittest.TestCase):
    def setUp(self):
        self.window = arcade.Window(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, "Test")
        self.game_view = GameView()
        self.window.show_view(self.game_view)

    def test_initial_setup(self):
        self.assertIsNotNone(self.game_view.player1_sprite)
        self.assertIsNotNone(self.game_view.player2_sprite)
        self.assertEqual(self.game_view.round_number, 1)

    def test_round_reset(self):
        initial_round = self.game_view.round_number
        self.game_view.reset_round()
        self.assertEqual(self.game_view.round_number, initial_round)

    def tearDown(self):
        self.window.close()

if __name__ == '__main__':
    unittest.main()