
class Test():
    def __init__(self):
        # LED strip configuration:
        self.score = 0

    def update(self, score):
        original = score
        score += 1
        print "original " + str(original)
        print "score " + str(score)
        return score

    def doUpdate(self):
        self.score = self.update(self.score)
        self.score = self.update(self.score)
        print "final score " + str(t.score)




t = Test()
t.doUpdate()


