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
    except GLib.Error:
        print('- no Signal process found, starting Signal')
        command = 'signal-cli -u {} daemon'.format(number).split()
        print('- Signal starting, waiting to connect')
        subprocess.Popen(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        while signal == None:
            try:
                signal = bus.get('org.asamk.Signal')
            except GLib.Error:
                pass

    print('- connected to Signal process')

    return signal
