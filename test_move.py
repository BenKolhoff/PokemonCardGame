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

    def test_str_representation(self):
        move = Move("Thunderbolt", 40, 2)
        expected_str = "Thunderbolt - 40 damage, cost 2"
        self.assertEqual(str(move), expected_str)

    def test_edge_case_values(self):
        # Testing zero values
        move_zero = Move("Zero Hit", 0, 0)
        self.assertEqual(move_zero.name, "Zero Hit")
        self.assertEqual(move_zero.damage, 0)
        self.assertEqual(move_zero.cost, 0)
        
        # Testing negative values if applicable; adjust the expected behavior if negatives should be sanitized
        move_negative = Move("Negative Impact", -10, -2)
        self.assertEqual(move_negative.name, "Negative Impact")
        self.assertEqual(move_negative.damage, -10)
        self.assertEqual(move_negative.cost, -2)
        
    def test_none_initialization(self):
        move = Move(None, None, None)
        self.assertEqual(move.name, "")
        self.assertEqual(move.damage, 0)
        self.assertEqual(move.cost, 0)

if __name__ == "__main__":
    unittest.main()
