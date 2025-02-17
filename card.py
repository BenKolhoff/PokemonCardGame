import json
from move import Move
from state import State

class Card:
    def __init__(self, name, type, hp, stage, weakness=None, retreat_cost=None, evolves_from=None):
        self.name = name
        self.type = type
        self.hp = hp
        self.stage = stage
        self.weakness = weakness
        self.retreat_cost = retreat_cost
        self.evolves_from = evolves_from
        self.energy = 0

    def attack(self, target, move):
        target.hp -= move.damage
        print(self.name, "used", move.name, "for", move.damage, "damage")
        print(target.name, "HP is now", target.hp)
        print()

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
        

    def attach_energy(self):
        self.energy += 1

    def retreat(self):
        if self.energy >= self.retreat_cost:
            # move from active to bench
            pass


