import unittest
import io
from unittest.mock import patch
from player import Player
from card import Card

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.card1 = Card("Bulbasaur", "Grass", 70, "Basic", "Fire", 2)
        self.card2 = Card("Charmander", "Fire", 60, "Basic", "Water", 1)
        self.player = Player([self.card1, self.card2])
    
    def test_initialization(self):
        self.assertIsNone(self.player.active_card)
        self.assertEqual(len(self.player.benched_cards), 0)
        self.assertEqual(len(self.player.hand), 0)
        self.assertEqual(len(self.player.deck), 2)
        self.assertEqual(len(self.player.discard), 0)
        self.assertEqual(self.player.points, 0)
    
    def test_set_active_card(self):
        self.player.hand.append(self.card1)
        self.player.set_active_card(0)
        self.assertEqual(self.player.active_card, self.card1)
        self.assertEqual(len(self.player.hand), 0)
    
    def test_set_active_card_non_integer(self):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.player.hand.append(self.card1)
            self.player.set_active_card("0")
            self.assertEqual(mock_stdout.getvalue().strip(), "Index must be an integer")
    
    def test_set_active_card_already_active(self):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.player.hand.append(self.card1)
            self.player.set_active_card(0)
            # add another card to hand to attempt change
            self.player.hand.append(self.card2)
            self.player.set_active_card(0)
            output_lines = mock_stdout.getvalue().strip().splitlines()
            self.assertEqual(output_lines[-1], "You already have an active card. You must retreat that first.")
    
    def test_set_active_card_empty_hand(self):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.player.set_active_card(0)
            self.assertEqual(mock_stdout.getvalue().strip(), "You cannot set an active card with an empty hand.")
    
    def test_set_active_card_index_out_of_bounds(self):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.player.hand.append(self.card1)
            self.player.set_active_card(5)
            self.assertEqual(mock_stdout.getvalue().strip(), "The specified index is out of bounds of your hand")
    
    def test_bench_card(self):
        self.player.bench_card(self.card2)
        self.assertIn(self.card2, self.player.benched_cards)
    
    def test_increase_points(self):
        self.player.increase_points()
        self.assertEqual(self.player.points, 1)
    
    def test_discard_card(self):
        self.player.hand.append(self.card1)
        self.player.discard_card(self.card1)
        self.assertIn(self.card1, self.player.discard)
        self.assertIsNone(self.player.active_card)
    
    def test_discard_benched_card(self):
        self.player.bench_card(self.card2)
        self.player.discard_card(self.card2)
        self.assertIn(self.card2, self.player.discard)
        self.assertNotIn(self.card2, self.player.benched_cards)
    
    def test_print_hand(self):
        self.player.hand.append(self.card1)
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.player.print_hand()
            self.assertEqual(mock_stdout.getvalue().strip(), str(self.card1).strip())
    
    def test_set_deck(self):
        new_deck = [self.card1, self.card2]
        self.player.set_deck(new_deck)
        self.assertEqual(self.player.deck, new_deck)
    
    def test_draw_card(self):
        self.player.draw_card()
        self.assertIn(self.card1, self.player.hand)
        self.assertEqual(len(self.player.deck), 1)
    
    def test_draw_card_empty_deck(self):
        # Set deck to empty to trigger draw_card edge-case.
        self.player.deck = []
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            try:
                self.player.draw_card()
            except IndexError:
                # If the implementation raises IndexError for empty deck, that's acceptable.
                pass
            self.assertTrue("Cannot draw, your deck is empty" in mock_stdout.getvalue().strip())

if __name__ == "__main__":
    unittest.main()
