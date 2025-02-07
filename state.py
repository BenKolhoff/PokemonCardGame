from player import Player

class State:
    def __init__(self, current_player=None):
        self.playerA = Player()
        self.playerB = Player()
        self.current_player = self.playerA if current_player is None else current_player

    '''
    Changes the current player to the opposite player.
    '''
    def change_player(self):
        self.current_player = self.playerA if self.current_player == self.playerB else self.playerB