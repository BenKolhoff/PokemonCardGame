import unittest
from move import Move

class TestMove(unittest.TestCase):
    def setUp(self):
        self.move1 = Move("Tackle", 20, 1)
        self.move2 = Move("Flamethrower", 90, 3)
    
    def test_initialization(self):
        self.assertEqual(self.move1.name, "Tackle")
        self.assertEqual(self.move1.damage, 20)
        self.assertEqual(self.move1.cost, 1)
        
        self.assertEqual(self.move2.name, "Flamethrower")
        self.assertEqual(self.move2.damage, 90)
        self.assertEqual(self.move2.cost, 3)
    
    def test_invalid_initialization(self):
        move = Move(123, "invalid", "wrong")
        self.assertEqual(move.name, "")
        self.assertEqual(move.damage, 0)
        self.assertEqual(move.cost, 0)

if __name__ == "__main__":
    unittest.main()
