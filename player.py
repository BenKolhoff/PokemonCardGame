class Player:
    def __init__(self, deck=[]):
        self.active_card = None
        self.benched_cards = []
        self.hand = []
        self.deck = deck if type(deck) == list else []
        self.discard = []
        self.points = 0

    '''
    Sets the player's active card if they specify a valid index and don't already have a card.
    '''
    def set_active_card(self, index):
        if self.active_card != None:
            print("You already have an active card. You must retreat that first.")
        elif type(index) != int:
            print("Index must be an integer")
        elif len(self.hand) == 0:
            print("You cannot set an active card with an empty hand.")
        elif index < 0 or index >= len(self.hand):
            print("The specified index is out of bounds of your hand")
        else:
            self.active_card = self.hand[index]
            self.hand.pop(index)
            print("Your active card is now " + self.active_card.name)

    def bench_card(self, card):
        self.benched_cards.append(card)

    def increase_points(self):
        self.points += 1

    def discard(self, card):
        self.discard.append(card)

        if card == self.active_card:
            self.active_card = None
        elif card in self.benched_cards:
            self.benched_cards.remove(card)
    
    '''
    Sets the deck of the player instance to the specified deck.
    '''
    def set_deck(self, deck):
        self.deck = deck
    
    '''
    Draws a card from the player's deck.
    '''
    def draw_card(self):
        if self.deck[0] == None:
            print("Cannot draw, your deck is empty")
            return

        deck_top = self.deck[0]
        self.hand.append(deck_top)
        self.deck.remove(deck_top)

    '''
    Prints the hand in a clean format.
    '''
    def print_hand(self):
        for card in self.hand:
            print(card)