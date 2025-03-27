'''
A class representing a move a card can use.

Attributes:
name (str) - The name of the move
damage (int) - The amount of damage done by the move
cost (str) - The cost of the move (in format "XX" where the first X is the amount and second is the type)
'''
class Move:
    def __init__(self, name, damage, cost):
        self.name = name if isinstance(name, str) else ""
        self.damage = damage if isinstance(damage, (int, float)) else 0
        self.cost = cost if isinstance(cost, int) else 0

    def __str__(self):
        return f"{self.name} - {self.damage} damage, cost {self.cost}"
