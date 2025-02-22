import unittest
from card import Card
from move import Move

class TestCard(unittest.TestCase):
    def setUp(self):
        self.card1 = Card("Bulbasaur", "Grass", 70, "Basic", "Fire", 2)
        self.card2 = Card("Charmander", "Fire", 60, "Basic", "Water", 1)
        self.move = Move("Vine Whip", 30, 2)
    
    def test_initialization(self):
        self.assertEqual(self.card1.name, "Bulbasaur")
        self.assertEqual(self.card1.type, "Grass")
        self.assertEqual(self.card1.hp, 70)
        self.assertEqual(self.card1.stage, "Basic")
        self.assertEqual(self.card1.weakness, "Fire")
        self.assertEqual(self.card1.retreat_cost, 2)
        self.assertEqual(self.card1.energy, 0)
    
    def test_attack(self):
        self.card1.attack(self.card2, self.move)
        self.assertEqual(self.card2.hp, 30)  # 60 - 30 = 30
    
    def test_attach_energy(self):
        self.card1.attach_energy()
        self.assertEqual(self.card1.energy, 1)
    
    def test_evolve(self):
        evolved_card = Card("Ivysaur", "Grass", 100, "Stage 1", "Fire", 3, "Bulbasaur")
        self.card1.evolve(evolved_card)
        self.assertEqual(self.card1.name, "Ivysaur")
        self.assertEqual(self.card1.hp, 100)
        self.assertEqual(self.card1.stage, "Stage 1")
    
    def test_retreat(self):
        self.card1.energy = 2
        self.card1.retreat()
        self.assertEqual(self.card1.energy, 2)  # Need to implement full logic for this

if __name__ == "__main__":
    unittest.main(verbosity=2)
