import json
from state import State

'''
The game itself, having fields for the state of the game and a masterlist of cards and moves.

Attributes:
pokemon (str{}) - A dictionary of all the different Pokemon and their associated values
moves (str{}) - A dictionary of all the different moves and their associated values
state (State) - A State instance owned by Game
'''
class Game:
    def __init__(self):
        with open('./data/Pokemon.json') as f:
            self.pokemon = json.load(f)
        with open('./data/Moves.json') as f:
            self.moves = json.load(f)

        self.state = State(self)