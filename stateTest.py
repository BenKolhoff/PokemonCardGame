import unittest
from state import State
from game import Game
from player import Player

class TestState(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.state = State(self.game)
    
    def test_initialization(self):
        self.assertIsInstance(self.state.playerA, Player)
        self.assertIsInstance(self.state.playerB, Player)
        self.assertIn(self.state.current_player, [self.state.playerA, self.state.playerB])
        self.assertEqual(len(self.state.playerA.deck), 53)  # 60 - 7 drawn cards
        self.assertEqual(len(self.state.playerB.deck), 53)
        self.assertEqual(len(self.state.playerA.hand), 7)
        self.assertEqual(len(self.state.playerB.hand), 7)
    
    def test_change_player(self):
        initial_player = self.state.current_player
        self.state.change_player()
        self.assertNotEqual(self.state.current_player, initial_player)
    
    def test_print_state(self):
        try:
            self.state.print_state()
            printed = True
        except Exception:
            printed = False
        self.assertTrue(printed)

if __name__ == "__main__":
    unittest.main()
