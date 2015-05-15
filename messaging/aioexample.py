#!/usr/bin/env python

import sys
# Add a logging handler so we can see the raw communication data
import logging
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

sys.path.append('..')

import time

import pusherclient

global pusher


def print_usage(filename):
    print("Usage: python %s <appkey> <secret>" % filename)

def channel_callback(data):
    print("Channel Callback: %s" % data)

def connect_handler(data):
    channel = pusher.subscribe(u'private-foosball_channel')

    channel.bind(u'game:queued', channel_callback)


if __name__ == '__main__':
    appid = '119859'
    key = '76abfc1ad02da9810a9d'
    secret ='07c4c701b5d1c864459d'

    pusher = pusherclient.Pusher(key, secret=secret)

    pusher.connection.bind(u'pusher:connection_established', connect_handler)
    pusher.connect()

    while True:
        time.sleep(1)
