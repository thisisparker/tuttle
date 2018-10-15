#! /usr/bin/env python3

import math
import time

import loadsignal
from logincoming import SignalMessage

from settings import NUMBER

def send(recipient, message):
    signal = loadsignal.load(NUMBER)
    signal.sendMessage(message, [], [recipient])
    print('- message sent')

    timestamp = math.floor(time.time()) * 1000

    msg = SignalMessage(timestamp, NUMBER, recipient, None, message, None)
    
    return msg
