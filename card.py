import json
from move import Move
from state import State

class Card:
    def __init__(self, name, card_type, hp, stage, weakness=None, retreat_cost=None, evolves_from=None):
        self.name = name if type(name) == str else None
        self.type = card_type if type(card_type) == str else None
        self.hp = hp if type(hp) == int else None
        self.stage = stage if type(stage) == int else None
        self.weakness = weakness if type(weakness) == str or weakness == None else None
        self.retreat_cost = retreat_cost if type(retreat_cost) == int or retreat_cost == None else None
        self.evolves_from = evolves_from if type(evolves_from) == str or evolves_from == None else None
        self.energy = 0

    '''
    Attacks another card (lowers their HP by the amount of damage caused by the used move).
    '''
    def attack(self, target, move):
        target.hp -= move.damage
        print(self.name, "used", move.name, "for", move.damage, "damage")
        print(target.name, "HP is now", target.hp)
        print()

    '''
    Evolves the card into the specified evolution.
    '''
    def evolve(self, new):
        if self.stage == "basic" and new.stage == "stage 1":
            if new.evolves_from == self.name:
                print(self.name, "evolved to", new.name)
                self = new
            else:
                print(self.name, "doesnt evolve from", new.name)
        elif self.stage == "stage 1" and new.stage == "stage 2":
            print(self.name, "evolved to", new.name)
            self = new
        else:
            print(self.stage, "can't evolve to a", new.stage)
        
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
        return self.name

