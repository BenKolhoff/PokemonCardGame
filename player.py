class Player:
    def __init__(self, active_card=None, benched_cards=[], hand=[], deck=[]):
        self.active_card = active_card
        self.benched_cards = benched_cards
        self.hand = hand
        self.deck = deck
    
    # Methods to implement:
    # set_active_card
    # bench_card
    # draw_card

    def set_active_card(self, card):
        self.active_card = card

    def bench_card(self, card):
        self.benched_cards.append(card)