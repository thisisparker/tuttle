#!/usr/bin/env python3

import json
import math
import os
import sqlite3
import time
import shlex
import shutil
import yaml

import magic
import pydbus

import loadsignal

from datetime import datetime
from subprocess import Popen, PIPE

from gi.repository import GLib

from settings import NUMBER, database

signalpath = os.path.join(os.path.expanduser('~'), '.config', 'signal')
sitepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

class SignalMessage:
    def __init__(self, timestamp, source, recipient, groupID, message, 
                 attachments, expires_in=None, seen_at=None, rowid=None):
        self.timestamp = timestamp
        self.source = source
        self.recipient = recipient
        self.groupID = groupID
        self.message = message
        self.expires_in = expires_in
        self.seen_at = seen_at
        self.rowid = rowid

        if attachments:
            self.attachments = attachments
        else:
            self.attachments = None

        if type(self.timestamp) == int:
            self.timestamp = datetime.utcfromtimestamp(
                    math.floor(self.timestamp/1000))

    def log_to_db(self, conn):
        conn.execute("""insert or replace into messages(
                            rowid, source, recipient, message, attachments,                                   timestamp, expires_in, seen_at)
                            values (?, ?, ?, ?, ?, ?, ?, ?)""",
                     (self.rowid, self.source, self.recipient, 
                         self.message, self.attachments, self.timestamp,
                         self.expires_in, self.seen_at))

def create_database():
    conn = sqlite3.connect(database)
    schema_script = """create table messages (
                    rowid       integer primary key,
                    source      text,
                    recipient   text,
                    groupID     text,
                    message     text,
                    attachments text,
                    timestamp   timestamp,
                    expires_in  integer,
                    seen_at     timestamp);"""
    conn.executescript(schema_script)
    conn.commit()
    conn.close()

def send_notifications():
    import sendmsg

    try:
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
    except OSError as err:
        config = {'notifications': [], 'autoresponder': ''}

    userlist = config['notifications']
    for user in userlist:
        sendmsg.send(user['number'], "There's a new message in your inbox.")

def send_autoresponse(sender):
    import sendmsg

    try:
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
    except OSError as err:
        config = {'autoresponder':''}

    conn = sqlite3.connect(database)
    seen_num = conn.execute('select count(*) from messages where source = ?',
            (sender,)).fetchone()[0]

    if config['autoresponder'] and not seen_num:
        sendmsg.send(sender, config['autoresponder'])

def log_msg(jsonmsg):
    timestamp = jsonmsg['timestamp']
    source = jsonmsg['source']
    groupID = jsonmsg['dataMessage']['groupInfo']
    message = jsonmsg['dataMessage']['message']
    try:
        attachments = jsonmsg['dataMessage']['attachments'][0]
    except IndexError as err:
        attachments = []
    try:
        expires_in = jsonmsg['dataMessage']['expiresInSeconds']
    except KeyError as err:
        expires_in = None

    conn = sqlite3.connect(database)

    if attachments:
        attachment_id = str(attachments['id'])
        new_filename = '-'.join([attachment_id, attachments['filename']])
        attach_path = os.path.join(sitepath, 'attachments')
        rec_path = os.path.join(signalpath, 'attachments', attachment_id)
        new_path = os.path.join(attach_path, new_filename)

        shutil.move(rec_path, new_path)

        attachments = new_filename

    msg = SignalMessage(timestamp, source, NUMBER, groupID, 
                        message, attachments, expires_in)

    send_autoresponse(msg.source)
    msg.log_to_db(conn)

    conn.commit()
    conn.close()

    send_notifications()

def signal_loop():
    print('- starting Signal instance')

    command = shlex.split('signal-cli -u {} daemon --json'.format(NUMBER))

    with Popen(command, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        print('- ready to receive messages')

        for line in p.stdout:
            jsonmsg = json.loads(line)['envelope']
            if (not jsonmsg['isReceipt'] and
                    (jsonmsg['dataMessage']['message'] or
                    jsonmsg['dataMessage']['attachments'])):
                log_msg(jsonmsg)

def main():
    if not os.path.isfile(database):
        print('- no logging database found, creating one now')
        create_database()

    print('- logging messages at {}'.format(database))

    signal_loop()

if __name__ == '__main__':
    main()
