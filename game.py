import json
from state import State

'''
The game itself, having fields for the state of the game and a masterlist of cards and moves.
'''
class Game:
    def __init__(self):
        with open('./data/Pokemon.json') as f:
            self.pokemon = json.load(f)
        with open('./data/Moves.json') as f:
            self.moves = json.load(f)

        self.state = State(self)