from player import Player
import random

'''
Represents the state of the game, not meant to be instantiated outside of the Game class.
'''
class State:
    def __init__(self, game, current_player=None):
        self.playerA = Player()
        self.playerB = Player()
        self.__player_list = [self.playerA, self.playerB]
        self.current_player = self.playerA if current_player is None else current_player

        # Randomly create the decks of each player
        for player in self.__player_list:
            deck = []
            for i in range(0, 60):    
                deck.append(game.pokemon[random.randint(0, len(game.pokemon) - 1)])
            
            player.set_deck(deck)

    '''
    Changes the current player to the opposite player.
    '''
    def change_player(self):
        self.current_player = self.playerA if self.current_player == self.playerB else self.playerB
    
    '''
    Print the state of the game in an easy-to-read format.
    '''
    def print_state(self):
        for i in range(0, len(self.__player_list)):
            print(f"--- Player {"A" if i == 0 else "B"} ---")
            print(f"Active Card: {self.__player_list[i].active_card}")
            print("Benched Cards: ", end='')
            for card in self.__player_list[i].benched_cards:
                print(f"{card} ", end='')
            print("")
            # Need way to handle hand so that the player calling this method can only see their hand
            print(f"Remaining cards in deck: {len(self.__player_list[i].deck)}")

