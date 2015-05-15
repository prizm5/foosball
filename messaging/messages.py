

class GameStarted(object):
    def __init__(self, id, player1, player1score, player2, player2score):
        self.Id = id
        self.Player1 = player1
        self.player1Score = player1score
        self.player2 = player2
        self.player2score = player2score

class GameEnded(GameStarted):
    def __init__(self, id, player1, player1score, player2, player2score):
        self.__init__(id, player1, player1score, player2, player2score)

class GoalScored(object):
    def __init__(self, id, player):
        self.Id = id
        self.Player = player

class GameQueued(object):
    def __init__(self,id):
        self.Id = id
