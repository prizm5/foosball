from enum import Enum
from messaging.messagecontroller import *
from sensor import *
from ledcontroller import *

class GameState(Enum):
    idle = 1
    instant_game = 2
    live_game = 3


class GameController(Configurable):
    def __init__(self, logger):
        Configurable.__init__(self, 'game.ini')
        self.state = GameState.idle
        self.player1score = 0
        self.player2score = 0

        sensor_config = self.ConfigSectionMap('sensor')
        sensors = SensorController()
        sensors.AddSensor(sensor_config['sensor1port'], self.player1scored, sensor_config['sensor1bounce'])
        sensors.AddSensor(sensor_config['sensor2port'], self.player2scored, sensor_config['sensor2bounce'])

        self.game = Game()
        self.messages = MessageController(logger, self.start_live_game)
        self.led = LedController()

    def start_instant_game(self):
        self.state = GameState.instant_game
        self.player1score = 0
        self.player2score = 0
        self.led.clear()

    def start_live_game(self, game):
        self.state = GameState.live_game
        self.led.clear()

    def player1scored(self, channel):
        self.game.player1Score += 1
        messages.GoalScored(self.game.id, self.game.player1)

    def player2scored(self, channel):
        self.game.player2Score += 1
        messages.GoalScored(self.game.id, self.game.player2)
