import jsonpickle
import pusher
from configurable import *
import pusherclient

from messages import *


class MessageController(Configurable):
    def __init__(self, logger, start_game_handler):
        Configurable.__init__(self, 'pusher.ini')
        config = self.ConfigSectionMap('pusher')
        app_id = config['appid']
        key = config['key']
        secret = config['secret']
        self.logger = logger
        self.game_handler = start_game_handler
        self.pusher = pusher.Pusher(app_id=app_id, key=key, secret=secret)
        self.channel = u'private-foosball_channel'
        self.client = pusherclient.Pusher(key, secret=secret) 
        self.client.connection.bind(u'pusher:connection_established', self.connect_handler)
        self.client.connect()
        logger.info("%s Initialized", __name__)

    def send_message(self, event, message):
        msg = jsonpickle.encode(message, unpicklable=False)
        self.pusher.trigger(self.channel, event, msg)

    def send_game_queued(self,id):
        m = GameQueued(id)
        self.send_message(u'client-game:queued', m)

    def send_goal_scored(self,id,player):
        m = GoalScored(id,player)
        self.send_message(u'client-game:goalscored', m)
        self.logger.info("%s scored a goal", player)

    def send_end_game(self, game):
        self.send_message(u'client-game:ended', game)

    def handle_game_start(self, data):
        msg = jsonpickle.decode(data)
        self.logger.info(u'client-game:started message received')
        self.logger.debug(msg)
        game = Game(msg['id'], msg['player1'], msg['player2'], msg['player1Score'], msg['player2Score'])
        self.logger.info("client-game:started message received")
        self.game_handler(game)

    def connect_handler(self, data):
        c = self.client.subscribe(self.channel)
        c.bind(u'client-game:started', self.handle_game_start)



