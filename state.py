from player import Player

class State:
    def __init__(self, current_player=None):
        self.playerA = Player()
        self.playerB = Player()
        self.current_player = self.playerA if current_player is None else current_player
        

    