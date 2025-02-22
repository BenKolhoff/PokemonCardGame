import unittest
from player import Player
from card import Card

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.card1 = Card("Bulbasaur", "Grass", 70, "Basic", "Fire", 2)
        self.card2 = Card("Charmander", "Fire", 60, "Basic", "Water", 1)
        self.player = Player([self.card1, self.card2])
    
    def test_initialization(self):
        self.assertEqual(self.player.active_card, None)
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
    
    def test_bench_card(self):
        self.player.bench_card(self.card2)
        self.assertIn(self.card2, self.player.benched_cards)
    
    def test_increase_points(self):
        self.player.increase_points()
        self.assertEqual(self.player.points, 1)
    
    def test_discard_card(self):
        self.player.hand.append(self.card1)
        self.player.discard_card(self.card1)  # Updated method name
        self.assertIn(self.card1, self.player.discard)  # Updated attribute name
        self.assertEqual(self.player.active_card, None)

    
    def test_set_deck(self):
        new_deck = [self.card1, self.card2]
        self.player.set_deck(new_deck)
        self.assertEqual(self.player.deck, new_deck)
    
    def test_draw_card(self):
        self.player.draw_card()
        self.assertIn(self.card1, self.player.hand)
        self.assertEqual(len(self.player.deck), 1)

if __name__ == "__main__":
    unittest.main()
