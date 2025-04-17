import unittest
from state import State
from game import Game
from player import Player
import io
import sys

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
        # No need to capture initial_energy since the inactive player starts at 0.
        self.state.change_player()
        self.assertNotEqual(self.state.current_player, initial_player)
        # The new current player's energy should now be 1 (0 + 1).
        self.assertEqual(self.state.current_player.energy, 1)
    
    def test_print_state(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            self.state.print_state()
        except Exception as ex:
            self.fail(f"print_state raised an Exception: {ex}")
        finally:
            sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Player", output)
    
    def test_get_player_list(self):
        players = self.state.get_player_list()
        self.assertEqual(len(players), 2)
        self.assertIn(self.state.playerA, players)
        self.assertIn(self.state.playerB, players)
    
    def test_activate_card_phase_default(self):
        # Verify that activate_card_phase is True by default
        self.assertTrue(self.state.activate_card_phase)
    
    def test_deck_hand_consistency(self):
        # Ensure that the total cards (deck + hand) equal 60 for each player.
        total_cards_playerA = len(self.state.playerA.deck) + len(self.state.playerA.hand)
        total_cards_playerB = len(self.state.playerB.deck) + len(self.state.playerB.hand)
        self.assertEqual(total_cards_playerA, 60)
        self.assertEqual(total_cards_playerB, 60)

if __name__ == "__main__":
    unittest.main()
