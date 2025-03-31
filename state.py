from card import Card
from move import Move
from player import Player
import random

'''
Represents the state of the game, not meant to be instantiated outside of the Game class.

Attributes:
playerA (Player) - An instance of the Player class
playerB (Player) - An instance of the Player class
current_player (Player) - The playe rwhose turn it is
activate_card_phase (bool) - A boolean which dictates whether or not it is the starting activation phase or not

Methods:
change_player -> None - Changes the current player to the opposite player
print_state -> None - Prints the current state of the game in an easy-to-read format
get_player_list -> Player[] - Returns the list of players
'''
class State:
    def __init__(self, game, activate_card_phase=True, current_player=None):
        self.playerA = Player('A')
        self.playerB = Player('B')
        self.__player_list = [self.playerA, self.playerB]
        self.current_player = self.playerA if current_player is None else current_player
        self.activate_card_phase = activate_card_phase if type(activate_card_phase) == bool else True

        # Randomly create the decks of each player
        for player in self.__player_list:
            deck = []
            for i in range(0, 60):  
                # Get data of a random object in the JSON card list, and then make a Card object from that
                card_data = game.pokemon[random.randint(0, len(game.pokemon) - 1)]
                new_card = Card(card_data['Name'], card_data['Type'], card_data['HP'], card_data['Stage'], 
                                card_data['Weakness'], card_data['Retreat'], None, None, player)
                
                if 'Moves' in card_data:
                    temp_moves = []
                    for move_name in card_data['Moves']:
                        for move in game.moves:
                            if move['Name'] == move_name:
                                temp_move = Move(move['Name'], move['Damage'], move['Cost'])
                                temp_moves.append(temp_move)
                    
                    new_card.moves = temp_moves

                deck.append(new_card)
            
            player.set_deck(deck)
        
        # Have each player automatically draw 7 cards
        for player in self.__player_list:
            for i in range(0, 7):
                player.draw_card()

    '''
    Changes the current player to the opposite player.

    return: None
    '''
    def change_player(self):
        self.current_player = self.playerA if self.current_player == self.playerB else self.playerB
    
    '''
    Print the state of the game in an easy-to-read format.

    return: None
    '''
    def print_state(self):
        for i in range(0, len(self.__player_list)):
            print(f"--- Player {"A" if i == 0 else "B"} ---{" (Current Turn)" if self.current_player == self.__player_list[i] else ""}")
            print(f"Active Card: {self.__player_list[i].active_card}")
            print("Benched Cards: ", end='')
            for card in self.__player_list[i].benched_cards:
                print(f"{card} ", end='')
            print(f"\nPoints: {self.__player_list[i].points}")
            print(f"Remaining cards in deck: {len(self.__player_list[i].deck)}")

    '''
    Returns the list of players.

    return: Player[]
    '''
    def get_player_list(self):
        return self.__player_list