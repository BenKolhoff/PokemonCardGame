class Card:
    def __init__(self, name, type, hp, stage, weakness, retreat_cost):
        self.name = name
        self.type = type
        self.hp = hp
        self.stage = stage
        self.weakness = weakness
        self.retreat_cost = retreat_cost

    def attack(self):
        pass

    def evolve(self, new):
        print(self.name)
        if self.stage == "basic" and new.stage == "stage 1":
            self = new
            print(self.name)
        elif self.stage == "stage 1" and new.stage == "stage 2":
            self = new

    def attach_energy(self):
        pass

    def retreat(self):
        pass


pikachu = Card("Pikachu", "electric", 70, "basic", "ground", 1)

raichu = Card("Raichu", "electric", 110, "stage 1", "ground", 1)

pikachu.evolve(raichu)


