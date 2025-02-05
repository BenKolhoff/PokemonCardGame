class Card:
    def __init__(self, name, type, hp, stage, weakness, retreat_cost, evolves_from):
        self.name = name
        self.type = type
        self.hp = hp
        self.stage = stage
        self.weakness = weakness
        self.retreat_cost = retreat_cost
        self.evolves_from = evolves_from
        self.energy = 0

    def attack(self):
        pass

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


pikachu = Card("Pikachu", "electric", 70, "basic", "ground", 1, None)
raichu = Card("Raichu", "electric", 110, "stage 1", "ground", 1, "Pikachu")
charmander = Card("Charmander", "fire", 70, "basic", "water", 1, None)
charmeleon = Card("Charmeleon", "fire", 110, "stage 1", "water", 2, "Charmander")
charizard = Card("Charizard", "fire", 200, "stage 2", "water", 2, "Charmeleon")

pikachu.evolve(raichu)

charmander.evolve(charmeleon)


