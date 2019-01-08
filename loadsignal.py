#! /usr/bin/env python3

import subprocess

import pydbus

from gi.repository import GLib

def load(number):
    bus = pydbus.SessionBus()

    print('- checking for Signal process')
    signal = None 
    try:
        signal = bus.get('org.asamk.Signal')
        print('- connected to Signal process')
        return signal
    except GLib.Error:
        print('- no Signal process found')
        return None
