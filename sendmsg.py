#! /usr/bin/env python3

import math
import sqlite3
import time

import loadsignal
from logincoming import SignalMessage

from settings import database, NUMBER

def send(recipient, message):
    signal = loadsignal.load(NUMBER)
    signal.sendMessage(message, [], [recipient])
    print('- message sent')

    timestamp = math.floor(time.time()) * 1000

    msg = SignalMessage(timestamp, NUMBER, recipient, None, message, None)

    conn = sqlite3.connect(database)

    msg.log_to_db(conn)
    print("- logging reply to db")

    conn.commit()
    conn.close()
