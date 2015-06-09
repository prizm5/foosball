from enum import Enum
from messagecontroller import *
from sensor import *
from ledcontroller import *
import time

from datetime import datetime
from datetime import timedelta

class GameState(Enum):
    idle = 1
    instant_game = 2
    live_game = 3


class GameController(Configurable):
    def __init__(self, logger):
        Configurable.__init__(self, '/home/pi/development/foosball/game.ini')
        self.logger = logger
        self.__state = GameState.idle
        self.player1score = 0
        self.player2score = 0
        self.last_action_time = datetime.now()

        sensor_config = self.ConfigSectionMap('sensor')
        sensors = SensorController(logger)

        sensors.AddSensor(sensor_config['sensor1port'], self.player1scored, sensor_config['sensor1bounce'])
        sensors.AddSensor(sensor_config['sensor2port'], self.player2scored, sensor_config['sensor2bounce'])

        sensors.AddButton(sensor_config['greenbuttonport'], self.start_instant_game, sensor_config['greenbuttonbounce'])
        sensors.AddButton(sensor_config['redbuttonport'], self.handle_red_button, sensor_config['redbuttonbounce'])

        self.game = Game()

        self.messages = MessageController(logger, self.start_live_game)

        self.led = LedController(logger)
        self.run_idle()
        logger.info("%s Initialized", __name__)

    def checkState(self):
        now = datetime.now()
        delta = timedelta(minutes=3)
        if self.last_action_time + delta < now:
            self.has_game_ended(True)

    def handle_red_button(self, channel):
        self.logger.info("Red button pushed")
        if self.__state != GameState.idle:
            if self.__state == GameState.live_game:
                self.messages.send_game_queued(self.game.id)
            self.__state = GameState.idle

    def start_instant_game(self, channel):
        self.logger.info("Green button pushed")
        if self.__state == GameState.idle:
            self.logger.info("New Instant Game Started")
            self.__state = GameState.instant_game
            self.game = Game()
            self.led.idle = False
            self.led.clear()
            self.led.flash_player_colors()

    def start_live_game(self, game):
        self.logger.info("Green button pushed")
        if self.__state == GameState.idle:
            self.logger.info("New Live Game Started")
            self.__state = GameState.live_game
            self.game = game
            self.led.idle = False
            self.led.clear()
            self.led.flash_player_colors()
            self.logger.info("New Live Game Started between %s and %s", self.game.player1, self.game.player2)

    def scored(self,player, playerid, score):
        if self.__state != GameState.idle:
            original = score
            self.logger.info("Player %s scored!", player)
            if self.__state == GameState.live_game:
                self.messages.send_goal_scored(self.game.id, player)
            score += 1
            for i in range(0, 6):
                if i % 2 == 0:
                    self.led.set_player_score(playerid, score)
                else:
                    self.led.set_player_score(playerid, original)
                time.sleep(.15)
            self.led.set_player_score(playerid, score)
            self.has_game_ended()
            self.last_action_time = datetime.now()
            return score

    def player1scored(self, channel):
        self.game.player1Score = self.scored(self.game.player1, 1, self.game.player1Score)

    def player2scored(self, channel):
        self.game.player2Score = self.scored(self.game.player2, 2, self.game.player2Score)

    def has_game_ended(self, end = False):
        if self.game.player1Score == 10 or self.game.player2Score == 10 or end:
            self.logger.info("Game has ended!")
            if self.__state == GameState.live_game:
                self.messages.send_end_game(self.game)
            self.__state = GameState.idle

    def run_idle(self):
        self.__state = GameState.idle
        while True:
            if self.__state == GameState.idle:
                self.led.idle = True
                # Color wipe animations.
                self.led.colorWipe(Color(255, 0, 0))  # Red wipe
                self.led.colorWipe(Color(0, 255, 0))  # Blue wipe
                self.led.colorWipe(Color(0, 0, 255))  # Green wipe
                # Theater chase animations.
                self.led.theaterChase(Color(127, 127, 127))  # White theater chase
                self.led.theaterChase(Color(127,   0,   0))  # Red theater chase
                self.led.theaterChase(Color(  0,   0, 127))  # Blue theater chase
                # Rainbow animations.
                self.led.rainbow()
                self.led.rainbowCycle()
                self.led.theaterChaseRainbow()
            else:
                self.led.idle = False

