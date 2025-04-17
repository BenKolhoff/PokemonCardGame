import unittest
import io
from unittest.mock import patch
from player import Player
from card import Card

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.card1 = Card("Bulbasaur", "Grass", 70, "Basic", "Fire", 2)
        self.card2 = Card("Charmander", "Fire", 60, "Basic", "Water", 1)
        self.player = Player('A', [self.card1, self.card2])
    
    def test_initialization(self):
        self.setUp()

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
        self.assertEqual(self.player.set_active_card("0"), "Index must be an integer")
    
    def test_set_active_card_already_active(self):
        self.player.hand.append(self.card1)
        self.player.set_active_card(0)
        self.player.hand.append(self.card2)
        self.assertEqual(self.player.set_active_card(0), "You already have an active card. You must retreat that first.")
    
    def test_set_active_card_empty_hand(self):
        self.assertEqual(self.player.set_active_card(0), "You cannot set an active card with an empty hand.")
    
    def test_set_active_card_index_out_of_bounds(self):
        self.player.hand.append(self.card1)
        self.assertEqual(self.player.set_active_card(5), "The specified index is out of bounds of your hand")
    
    def test_bench_card_empty_hand(self):
        self.player.bench_card(0)
        self.assertEqual(self.player.bench_card(0), "You cannot bench a card with an empty hand.")
    
    def test_bench_card(self):
        self.player.hand = [self.card1, self.card2]
        self.player.bench_card(1)
        self.assertIn(self.card2, self.player.benched_cards)
    
    def test_bench_card_non_basic(self):
        non_basic_card = Card("Ivysaur", "Grass", 80, "Stage 1", "Fire", 3, "Bulbasaur")
        self.player.hand.append(non_basic_card)
        result = self.player.bench_card(0)
        self.assertEqual(result, "Only basic cards can be benched")
    
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
        self.assertEqual(self.player.draw_card(), "Cannot draw, your deck is empty")

    def test_set_active_from_bench_valid(self):
        # Move a basic card to the bench.
        self.player.hand.append(self.card1)
        self.player.bench_card(0)
        result = self.player.set_active_from_bench(0)
        self.assertEqual(result, "Your active card is now " + self.card1.name)
        self.assertEqual(self.player.active_card, self.card1)
        self.assertNotIn(self.card1, self.player.benched_cards)

    def test_set_active_from_bench_non_integer(self):
        self.assertEqual(self.player.set_active_from_bench("0"), "Index must be an integer")

    def test_set_active_from_bench_empty_bench(self):
        self.assertEqual(self.player.set_active_from_bench(0), "You cannot set an active card because your bench is empty.")

    def test_set_active_from_bench_index_out_of_bounds(self):
        self.player.hand.append(self.card1)
        self.player.bench_card(0)
        self.assertEqual(self.player.set_active_from_bench(5), "The specified index is out of bounds of your bench")

    def test_set_active_from_bench_non_basic(self):
        # Create a card that is not Basic.
        non_basic_card = Card("Ivysaur", "Grass", 80, "Stage 1", "Fire", 3, "Bulbasaur")
        # Manually add to bench bypassing bench_card method.
        self.player.benched_cards.append(non_basic_card)
        self.assertEqual(self.player.set_active_from_bench(0), "Only basic cards can be set as active.")

if __name__ == "__main__":
    unittest.main()
