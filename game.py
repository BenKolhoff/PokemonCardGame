import json
from state import State

'''
The game itself, having fields for the state of the game and a masterlist of cards and moves.
'''
class Game:
    def __init__(self):
        with open('Pokemon.json') as f:
            self.pokemon = json.load(f)
        with open('Moves.json') as f:
            self.moves = json.load(f)

        self.state = State(self)