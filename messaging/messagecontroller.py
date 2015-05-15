import jsonpickle
from pusher import Pusher
from messages import *


class MessageController(object):
    def __init__(self, appid, key, secret):
        self.pusher = Pusher(app_id=appid, key=key, secret=secret)

    def SendMessage(message):
        oneway = jsonpickle.encode(message, unpicklable=False)
        pusher.trigger(u'a_channel', u'an_event', oneway)



m = GameStarted(1,'nils',0,'steve',0)

mc = MessageController()
