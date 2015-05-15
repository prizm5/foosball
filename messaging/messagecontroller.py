import jsonpickle
import ConfigParser
import os.path
import messages
import pusher
import time

import pusherclient


import sys
# Add a logging handler so we can see the raw communication data
import logging
root = logging.getLogger()
root.setLevel(logging.ERROR)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)




from messages import *

class Configurable(object):
    def __init__(self):
        fname = 'pusher.ini'
        if os.path.isfile(fname):
            self.Config = ConfigParser.ConfigParser()
            self.Config.read(fname)
        else:
            raise ('config not found')

    def ConfigSectionMap(self, section):
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                dict1[option] = self.Config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1


class MessageController(Configurable):
    def __init__(self):
        Configurable.__init__(self)
        appid = self.ConfigSectionMap('pusher')['appid']
        key = self.ConfigSectionMap('pusher')['key']
        secret = self.ConfigSectionMap('pusher')['secret']
        self.pusher = pusher.Pusher(app_id=appid, key=key, secret=secret)
        self.channel = u'private-foosball_channel'
        self.client = pusherclient.Pusher(key, secret=secret) 
        self.client.connection.bind(u'pusher:connection_established', self.connect_handler)
        self.client.connect()

    def SendMessage(self, event, message):
        oneway = jsonpickle.encode(message, unpicklable=False)
        self.pusher.trigger(self.channel,event, oneway)

    def SendGameQueued(self,id):
        m = GameQueued(id)
        self.SendMessage(u'game:queued',m)

    def SendGoalScored(self,id,player):
        m = GoalScored(id,player)
        self.SendMessage(u'game:goalscored',m)


    def SendEndGame(self, game):
        self.SendMessage(u'game:ended',game)


    def handleGameStart(self, data):
        msg = jsonpickle.decode(data)
        game = Game(msg['id'],msg['player1'],msg['player2'],msg['player1Score'],msg['player2Score'])
        print("Game Started between " + game.player1 + " and " + game.player2)

    def connect_handler(self, data):
        c = self.client.subscribe(self.channel)
        c.bind(u'client-game:started',self.handleGameStart)


mc = MessageController()

while True:
    #game = Game(1,6,10)
    #mc.SendGoalScored(game.id, game.player1)
    time.sleep(1)

