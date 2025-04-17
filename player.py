'''
A class representing a player of the game.

Attributes:
active_card (Card) - The player's active card
benched_cards (Card[]) - A list of Cards on the player's bench
hand (Card[]) - The hand of the player (a list of Cards)
deck (Card[]) - The player's deck (a list of cards)
discard (Card[]) - The player's discard "pile"
points (int) - The amount of points the player has

Methods:
set_active_card(index: int) -> None - Sets the player's active card if they specify a valid index and don't already have a card
set_active_from_bench(index: int) -> None - Sets the player's active card from the bench if they specify a valid index and don't already have a card
bench_card(card: Card) -> None - Moves the given card to the player's bench
increase_points -> None - Increases the points of the player by 1
discard_card(card: Card) -> None - Moves the card to the player's discard "pile" (the discard attribute)
set_deck(deck: Card[]) -> None - Sets the deck of the player instance to the specified deck
draw_card -> None - Draws a card from the player's deck
print_hand -> None - Prints the hand in a clean format
'''
class Player:
    def __init__(self, name, deck=[]):
        self.name = name
        self.active_card = None
        self.benched_cards = []
        self.hand = []
        self.deck = deck if type(deck) == list else []
        self.discard = []
        self.points = 0
        self.energy = 0

    '''
    Sets the player's active card if they specify a valid index and don't already have a card.

    index (int) - The index of the card to become the active card

    return: None
    '''
    def set_active_card(self, index):
        if self.active_card is not None:
            print("You already have an active card. You must retreat that first.")
        elif type(index) != int:
            print("Index must be an integer")
        elif len(self.hand) == 0:
            print("You cannot set an active card with an empty hand.")
        elif index < 0 or index >= len(self.hand):
            print("The specified index is out of bounds of your hand")
        elif self.hand[index].stage != "Basic":
            print("Only basic cards can be set as active.")
        else:
            self.active_card = self.hand[index]
            self.hand.pop(index)
            print("Your active card is now " + self.active_card.name)

    '''
    Sets the player's active card from the bench if they specify a valid index and don't already have a card.

    index (int) - The index of the card to become the active card

    return: None
    '''
    def set_active_from_bench(self, index):
        if self.active_card is not None:
            print("You already have an active card. You must retreat that first.")
        elif type(index) != int:
            print("Index must be an integer")
        elif len(self.benched_cards) == 0:
            print("You cannot set an active card because your bench is empty.")
        elif index < 0 or index >= len(self.benched_cards):
            print("The specified index is out of bounds of your bench")
        elif self.benched_cards[index].stage != "Basic":
            print("Only basic cards can be set as active.")
        else:
            self.active_card = self.benched_cards[index]
            self.benched_cards.pop(index)
            print("Your active card is now " + self.active_card.name)

    '''
    Moves the given card to the player's bench.

    card (Card) - The card to bench

    return: None    
    '''
    def bench_card(self, index):
        if type(index) != int:
            print("Index must be an integer")
        elif len(self.hand) == 0:
            print("You cannot set an active card with an empty hand.")
        elif index < 0 or index >= len(self.hand):
            print("The specified index is out of bounds of your hand")
        else:
            card = self.hand[index]
            if card.stage != "Basic":
                print("Only basic cards can be benched")
            else:
                self.benched_cards.append(card)
                self.hand.pop(index)

    '''
    Increases the points of the player by 1.

    return: None
    '''
    def increase_points(self):
        self.points += 1

    '''
    Moves the card to the player's discard "pile" (the discard attribute).

    card (Card) - The card to discard

    return: None
    '''
    def discard_card(self, card):
        self.discard.append(card)

        if card == self.active_card:
            self.active_card = None
        elif card in self.benched_cards:
            self.benched_cards.remove(card)
    
    '''
    Sets the deck of the player instance to the specified deck.

    deck (Card[]) - The deck to set the player's deck to

    return: None
    '''
    def set_deck(self, deck):
        self.deck = deck
    
    '''
    Draws a card from the player's deck.

    return: None
    '''
    def draw_card(self):
        if not self.deck:  # Check if the deck is empty
            print("Cannot draw, your deck is empty")
            return

        deck_top = self.deck[0]
        self.hand.append(deck_top)
        self.deck.remove(deck_top)

    '''
    Prints the hand in a clean format.

    return: None
    '''
    def print_hand(self):
        for card in self.hand:
            print(card)