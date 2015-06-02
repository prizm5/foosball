from enum import Enum
from messagecontroller import *
from sensor import *
from ledcontroller import *
import time

class GameState(Enum):
    idle = 1
    instant_game = 2
    live_game = 3


class GameController(Configurable):
    def __init__(self, logger):
        Configurable.__init__(self, 'game.ini')
        self.logger = logger
        self.state = GameState.idle
        self.player1score = 0
        self.player2score = 0

        sensor_config = self.ConfigSectionMap('sensor')
        sensors = SensorController(logger)

        sensors.AddSensor(sensor_config['sensor1port'], self.player1scored, sensor_config['sensor1bounce'])
        sensors.AddSensor(sensor_config['sensor2port'], self.player2scored, sensor_config['sensor2bounce'])

        sensors.AddButton(sensor_config['greenbuttonport'], self.start_instant_game, sensor_config['greenbuttonbounce'])
        sensors.AddButton(sensor_config['redbuttonport'], self.handle_red_button, sensor_config['redbuttonbounce'])

        self.game = Game()

        self.messages = MessageController(logger, self.start_live_game)

        self.led = LedController(logger)
        time.sleep(.25)
        self.run_idle()
        logger.info("%s Initialized", __name__)

    def handle_red_button(self, channel):
        self.logger.info("Red button pushed")
        if self.state != GameState.idle:
            if self.state == GameState.live_game:
                self.messages.send_game_queued(self.game.id)
            self.state = GameState.idle
            self.led.flash_player_colors()
            self.led.clear()
            self.led.idle = True
            self.run_idle()

    def start_instant_game(self, channel):
        self.logger.info("Green button pushed")
        if self.state == GameState.idle:
            self.logger.info("New Instant Game Started")
            self.state = GameState.instant_game
            self.game = Game()
            self.led.idle = False
            self.led.clear()
            self.led.flash_player_colors()

    def start_live_game(self, game):
        self.logger.info("New Live Game Started")
        self.state = GameState.live_game
        self.game = game
        self.led.idle = False
        self.led.clear()
        self.led.flash_player_colors()
        self.logger.info("New Live Game Started between %s and %s", self.game.player1, self.game.player2)

    def player1scored(self, channel):
        if self.state != GameState.idle:
            self.logger.info("Player %s scored!", self.game.player1)
            if self.state == GameState.live_game:
                self.messages.send_goal_scored(self.game.id, self.game.player1)
            self.game.player1Score += 1
            self.led.set_player_score(1, self.game.player1Score)
            self.has_game_ended()

    def player2scored(self, channel):
        if self.state != GameState.idle:
            self.logger.info("Player %s scored!", self.game.player2)
            if self.state == GameState.live_game:
                self.messages.send_goal_scored(self.game.id, self.game.player2)
            self.game.player2Score += 1
            self.led.set_player_score(2, self.game.player2Score)
            time.sleep(.25)
            self.has_game_ended()

    def has_game_ended(self):
        if self.game.player1Score == 10 or self.game.player2Score == 10:
            self.logger.info("Game has ended!")
            if self.state == GameState.live_game:
                self.messages.send_end_game(self.game)
            self.state = GameState.idle
            self.led.flash_player_colors()
            self.led.clear()
            self.led.idle = True
            self.run_idle()

    def run_idle(self):
        while True:
            if self.state != GameState.idle:
                break
            # Color wipe animations.
            self.led.colorWipe(Color(255, 0, 0))  # Red wipe
            self.led.colorWipe(Color(0, 255, 0))  # Blue wipe
            self.led.colorWipe(Color(0, 0, 255))  # Green wipe
            time.sleep(.025)
            # Theater chase animations.
            #self.led.theaterChase(Color(127, 127, 127))  # White theater chase
            #self.led.theaterChase(Color(127,   0,   0))  # Red theater chase
            #self.led.theaterChase(Color(  0,   0, 127))  # Blue theater chase
            # Rainbow animations.
            #self.led.rainbow()
            #self.led.rainbowCycle()
            #self.led.theaterChaseRainbow()


