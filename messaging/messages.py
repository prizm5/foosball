

class Game(object):
    def __init__(self, id, player1, player2, player1score, player2score):
        self.id = id
        self.player1 = 'player1'
        self.player1Score = player1score
        self.player1Color = '5DFC0A'
        self.player2 = 'player2'
        self.player2Score = player2score
        self.player2Color = '05E9FF'


class GoalScored(object):
    def __init__(self, id, player):
        self.Id = id
        self.Player = player


class GameQueued(object):
    def __init__(self,id):
        self.Id = id
