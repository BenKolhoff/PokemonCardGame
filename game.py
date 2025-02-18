import json
from state import State

'''
The game itself, having fields for the state of the game and a masterlist of cards and moves.
'''
class Game:
    def __init__(self):
        self.state = State()
        with open('Pokemon.json') as f:
            self.pokemon = json.load(f)
        with open('Moves.json') as f:
            self.moves = json.load(f)
    
    def instantiate_cards():
        pass

    def instantiate_moves():
        pass