from move import Move
from player import Player

'''
A class representing Pokemon cards.

Attributes
name (str) - The name of the card.
card_type (str) - The type of the card.
hp (int) - The starting health of the card.
weakness (str) - The card's type weakness.
retreat_cost (int) - The cost to retreat the card.
evolves_from (str) - The name of the card this card evolves from.
moves (Move[]) - The list of moves the card can use.
owner (Player) - The player who owns this card.

Methods
attack (target: Card, move: Move) -> None - Attacks the target with the specified move.
evolve (new: Card) -> None - Evolves the card into the specified card.
take_damage (amount: int) -> None - Subtracts the specified amount from the card's HP.
attach_energy -> None - Increases the energy of this card by 1.
retreat -> None - Retreats the card to the owner's bench.
update_name -> None - Updates the name to show the amount of energy the card currently has.
'''
class Card:
    def __init__(self, name, card_type, hp, stage, weakness=None, retreat_cost=None, evolves_from=None, moves=[], owner=None):
        self.name = name if type(name) == str else None
        self.type = card_type if type(card_type) == str else None
        self.hp = hp if type(hp) == int else None
        self.stage = stage if type(stage) == str else None
        self.weakness = weakness if type(weakness) == str or weakness == None else None
        self.retreat_cost = retreat_cost if type(retreat_cost) == int or retreat_cost == None else None
        self.evolves_from = evolves_from if type(evolves_from) == str or evolves_from == None else None
        self.energy = 0
        self.moves = moves if type(moves) == list else []
        self.owner = owner if isinstance(owner, Player) else None

        if len(self.moves) == 0:
            self.moves.append(Move("Attack", 50, '1N'))

    '''
    Attacks another card (lowers their HP by the amount of damage caused by the used move).

    target (Card) - The target card to attack
    move (Move) - The move the card will use

    return: None
    '''
    def attack(self, target, move):
        if target is None:
            return "Opponent has no active card, you must pass)"
        elif move is None:
            return "Invalid move"
        elif self.energy < move.cost:
            return "Not enough energy"

        target_is_weak = target.weakness == self.type
        damage = int(move.damage * 1.5) if target_is_weak else move.damage
        target.take_damage(damage)
        msg = f"{self.name} used {move.name} for {damage} damage" + (" (1.5x!)" if target_is_weak else "")
        msg += f"\n{target.name} HP is now {target.hp}"
        if target.owner.active_card is None:
            self.owner.increase_points()
        
        self.energy -= move.cost
        self.update_name()
        
        return msg

    '''
    Evolves the card into the specified evolution.

    new (Card) - The card to evolve into (must be equivalent to this card's "evolves_from" value)

    return: None
    '''
    def evolve(self, new):
        if self.stage == "Basic" and new.stage == "Stage 1" and new.evolves_from == self.name:
            print(f"{self.name} evolved into {new.name}")
            self.name = new.name
            self.type = new.type
            self.hp = new.hp
            self.stage = new.stage
            self.weakness = new.weakness
            self.retreat_cost = new.retreat_cost
            self.evolves_from = new.evolves_from
        elif self.stage == "Stage 1" and new.stage == "Stage 2" and new.evolves_from == self.name:
            print(f"{self.name} evolved into {new.name}")
            self.name = new.name
            self.type = new.type
            self.hp = new.hp
            self.stage = new.stage
            self.weakness = new.weakness
            self.retreat_cost = new.retreat_cost
            self.evolves_from = new.evolves_from
        else:
            print(f"{self.name} cannot evolve into {new.name}")

    '''
    Subtracts the specified damage from the card's HP, and discards it if its HP falls below 0.

    amount (int) - The amount of damage to be subtracted from this card's HP

    return: None
    '''
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        if self.hp == 0 and self.owner is not None:
            self.owner.discard_card(self)

    '''
    Attaches energy to this card (increases energy by one).

    return: None
    '''
    def attach_energy(self):
        self.energy += 1
        self.update_name()

    '''
    Moves the card from being "active" to the bench.

    return: None
    '''
    def retreat(self):
        if self.energy >= self.retreat_cost:
            # move from active to bench
            pass

    '''
    Updates the name to show the amount of energy the card currently has.

    return: None
    '''
    def update_name(self):
        self.name = f"{"*" * self.energy}{self.name}"

    def __str__(self):
        card_str = f"{self.name}::"
        for move in self.moves:
            card_str += str(move) + " "

        return card_str

