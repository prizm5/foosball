
class Test():


    @staticmethod
    def test_range(score):
        for i in range(0, 10):
            if i < score:
                v = 1
            else:
                v = 0
            print "i: " + str(i) + " val: " + str(v)


t = Test()
t.test_range(2)


