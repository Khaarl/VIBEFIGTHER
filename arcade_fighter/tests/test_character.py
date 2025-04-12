import unittest
from src.character import Character
from src import constants as C

class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.player = Character(player_num=1)

    def test_initial_state(self):
        self.assertEqual(self.player.state, C.STATE_IDLE)
        self.assertEqual(self.player.hp, C.PLAYER_START_HP)

    def test_take_damage(self):
        initial_hp = self.player.hp
        self.player.take_damage(10)
        self.assertEqual(self.player.hp, initial_hp - 10)
        self.assertEqual(self.player.state, C.STATE_HIT)

    def test_death_state(self):
        self.player.take_damage(self.player.hp)
        self.assertEqual(self.player.state, C.STATE_DEAD)
        self.assertEqual(self.player.hp, 0)

if __name__ == '__main__':
    unittest.main()