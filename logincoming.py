#!/usr/bin/env python3

import mimetypes
import math
import os
import sqlite3
import time
import subprocess
import shutil

import magic
import pydbus

import loadsignal

from datetime import datetime

from gi.repository import GLib

from settings import NUMBER, database

sitepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

class SignalMessage:
    def __init__(self, timestamp, source, recipient, groupID, message, 
                 attachments, rowid=None):
        self.timestamp = timestamp
        self.source = source
        self.recipient = recipient
        self.groupID = groupID
        self.message = message
        self.rowid = rowid

        if attachments:
            self.attachments = attachments
        else:
            self.attachments = None

        if type(self.timestamp) == int:
            self.timestamp = datetime.utcfromtimestamp(math.floor(self.timestamp/1000))

    def log_to_db(self, conn):
        conn.execute("""insert into messages(
                     source, recipient, message, attachments, timestamp)
                     values (?, ?, ?, ?, ?)""",
                     (self.source, self.recipient, self.message, 
                         self.attachments, self.timestamp))

def create_database():
    conn = sqlite3.connect(database)
    schema_script = """create table messages (
                    rowid       integer primary key,
                    source      text,
                    recipient   text,
                    groupID     text,
                    message     text,
                    attachments text,
                    timestamp   timestamp);"""
    conn.executescript(schema_script)
    conn.commit()
    conn.close()

def log_msg(timestamp, source, groupID, message, attachments):
    conn = sqlite3.connect(database)

    if attachments and '.config' in attachments[0]:
        attachpath = os.path.join(sitepath, 'attachments')
        
        rec_path = attachments[0]
        
        guessed_mimetype = magic.from_file(rec_path, mime=True)
        long_mimetypes_dict = {**mimetypes.types_map, **mimetypes.common_types}
        del long_mimetypes_dict['.jpe'] # annoying, but these are just
        del long_mimetypes_dict['.mp2'] # unlikely extensions, so skip 'em.
        guessed_ext = next((ext for ext in long_mimetypes_dict if
                       long_mimetypes_dict.get(ext) == guessed_mimetype), 
                       '.attach')

        filename = os.path.basename(rec_path) + guessed_ext
        shutil.move(rec_path, os.path.join(attachpath, filename))
        attachments = filename

    msg = SignalMessage(timestamp, source, NUMBER, groupID, 
                        message, attachments)
    msg.log_to_db(conn)

    conn.commit()
    conn.close()

def main():
    if not os.path.isfile(database):
        print('- no logging database found, creating one now')
        create_database()

    print('- logging messages at {}'.format(database))

    signal = loadsignal.load(NUMBER)    

    signal.onMessageReceived = log_msg

    print('- ready to receive messages')

    loop = GLib.MainLoop()
    loop.run()

if __name__ == '__main__':
    main()
