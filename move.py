class Move:
    def __init__(self, name, damage, cost):
        self.name = name if type(name) == str else ''
        self.damage = damage if type(damage) == int else 0
        self.cost = cost if type(cost) == int else 0
    
    def use(self):
        pass
