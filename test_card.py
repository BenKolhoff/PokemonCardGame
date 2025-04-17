import unittest
from card import Card
from move import Move
import io
from unittest.mock import patch

class TestCard(unittest.TestCase):
    def setUp(self):
        self.card1 = Card("Bulbasaur", "Grass", 70, "Basic", "Fire", 2)
        self.card2 = Card("Charmander", "Fire", 60, "Basic", "Water", 1)
        self.card3 = Card("Ivysaur", "Grass", 100, "Stage 1", "Fire", 3, "Bulbasaur")
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
        # Create a dummy owner with an active_card attribute.
        class DummyOwner:
            def __init__(self, card):
                self.active_card = card

        # Assign the dummy owner to card2.
        self.card2.owner = DummyOwner(self.card2)
        
        self.card1.energy = 2
        self.card1.attack(self.card2, self.move)
        self.assertEqual(self.card2.hp, 30)  # 60 - 30 = 30

    def test_attack_no_target(self):
        self.card1.energy = self.move.cost
        self.assertEqual(
            self.card1.attack(None, self.move),
            "Opponent has no active card, you must pass)"
        )

    def test_attack_invalid_move(self):
        self.card1.energy = self.move.cost
        self.assertEqual(
            self.card1.attack(self.card2, None),
            "Invalid move"
        )

    def test_attack_not_enough_energy(self):
        self.card1.energy = 0
        self.assertEqual(
            self.card1.attack(self.card2, self.move),
            "Not enough energy"
        )

    def test_attack_weakness_multiplier(self):
        # make card2 weak to card1
        self.card2.weakness = self.card1.type
        self.card1.energy = self.move.cost
        result = self.card1.attack(self.card2, self.move)
        # damage should be 1.5×
        expected_damage = int(self.move.damage * 1.5)
        self.assertIn(f"for {expected_damage} damage", result)
        self.assertIn("(1.5x!)", result)
    
    def test_attach_energy(self):
        self.card1.attach_energy()
        self.assertEqual(self.card1.energy, 1)
    
    def test_evolve(self):
        evolved_card = Card("Ivysaur", "Grass", 100, "Stage 1", "Fire", 3, "Bulbasaur")
        self.card1.evolve(evolved_card)
        self.assertEqual(self.card1.name, "Ivysaur")
        self.assertEqual(self.card1.hp, 100)
        self.assertEqual(self.card1.stage, "Stage 1")

    def test_evolve_stage1(self):
        evolved_card = Card("Venasaur", "Grass", 340, "Stage 2", "Fire", 4, "Ivysaur")
        self.card3.evolve(evolved_card)
        self.assertEqual(self.card3.name, "Venasaur")
        self.assertEqual(self.card3.hp, 340)
        self.assertEqual(self.card3.stage, "Stage 2")
    
    def test_evolve_invalid(self):
        # try to evolve into something not matching evolves_from
        bad = Card("Bar", "Type", 10, "Stage 2", None, None, "Other")
        with patch('sys.stdout', new_callable=io.StringIO) as out:
            self.card1.evolve(bad)
        self.assertIn("cannot evolve into", out.getvalue())

    def test_retreat(self):
        self.card1.energy = 2
        self.card1.retreat()
        self.assertEqual(self.card1.energy, 2)  # Need to implement full logic for this

    def test_retreat_no_energy(self):
        # retreat is a no-op if you don't meet retreat_cost
        before = self.card1.energy
        self.card1.retreat()
        self.assertEqual(self.card1.energy, before)

    def test_take_damage(self):
        self.card1.take_damage(30)
        self.assertEqual(self.card1.hp, 40)  # 70 - 30 = 40

        self.card1.take_damage(50)
        self.assertEqual(self.card1.hp, 0)  # Cannot go below 0

    def test_str(self):
        move = Move("Tackle", 40, 1)
        card = Card("Pikachu", "Electric", 60, "Basic", moves=[move])
        self.assertIn("Pikachu::Tackle", str(card))
    
    def test_update_name(self):
        # energy increases prefix stars
        self.card1.card_name = "Foo"
        self.card1.energy = 2
        self.card1.update_name()
        self.assertEqual(self.card1.name, "**Foo")

    def test_take_damage_with_owner(self):
        # Create a dummy player with a discard pile.
        class DummyPlayer:
            def __init__(self):
                self.discard = []
            def discard_card(self, card):
                self.discard.append(card)

        dummy_owner = DummyPlayer()
        self.card1.owner = dummy_owner
        self.card1.take_damage(70)  # Knock out the card
        self.assertEqual(self.card1.hp, 0)
        self.assertIn(self.card1, dummy_owner.discard)

    def test_move_invalid_types(self):
        # Test move initialization with invalid types.
        move = Move(123, "not int", None)
        self.assertEqual(move.name, '')
        self.assertEqual(move.damage, 0)
        self.assertEqual(move.cost, 0)

if __name__ == "__main__":
    unittest.main()
