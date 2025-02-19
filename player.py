class Player:
    def __init__(self, deck=[]):
        self.active_card = None
        self.benched_cards = []
        self.hand = []
        self.deck = deck if type(deck) == list else []
        self.discard = []
        self.points = 0
    
    # Methods to implement:
    # set_active_card
    # bench_card
    # draw_card

    def set_active_card(self, card):
        self.active_card = card

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
    
    def set_deck(self, deck):
        self.deck = deck
    
    def draw_card(self):
        if self.deck[0] == None:
            print("Cannot draw, your deck is empty")
            return

        deck_top = self.deck[0]
        self.hand.append(deck_top)
        self.deck.remove(deck_top)

    def print_hand(self):
        for card in self.hand:
            print(card['Name'], end=' ')
        
        print("")