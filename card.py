from move import Move
from player import Player

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
    '''
    def attack(self, target, move):
        if target == None:
            print("Error: Invalid target (if the target player has no active card, you must pass)")
            return
        elif move == None:
            print("Error: Invalid move")
            return

        target_is_weak = target.weakness == self.type
        damage = int(move.damage * 1.5) if target_is_weak else move.damage 
        target.take_damage(damage)
        print(self.name, "used", move.name, "for", damage, "damage", f"{"(1.5x!)" if target_is_weak else ""}")
        print(target.name, "HP is now", target.hp)
        
        if target.owner.active_card == None:
            self.owner.increase_points()
            print(f"Current player now has: {self.owner.points} points")
        print()

    '''
    Evolves the card into the specified evolution.
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
    '''
    def take_damage(self, amount):
        if type(amount) == int:
            self.hp -= amount
            self.hp = max(self.hp, 0)

            if self.hp <= 0:
                self.owner.discard_card(self)

    '''
    Attaches energy to this card (increases energy by one).
    '''
    def attach_energy(self):
        self.energy += 1

    '''
    Moves the card from being "active" to the bench.
    '''
    def retreat(self):
        if self.energy >= self.retreat_cost:
            # move from active to bench
            pass

    def __str__(self):
        card_str = f"{self.name}::"
        for move in self.moves:
            card_str += str(move) + " "

        return card_str

