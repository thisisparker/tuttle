#!/bin/env python3

import os
import sqlite3

from settings import database
from logincoming import sitepath

def single_msg(msgid):
    conn = sqlite3.connect(database)

    attachment = conn.execute(
            'select attachments from messages where rowid = ?',
            [msgid]).fetchone()
    attachment = attachment[0]
    if attachment:
        attachments_dir = os.path.join(sitepath, 'attachments')
        attachment_path = os.path.join(attachments_dir, attachment)
        os.remove(attachment_path)
    
    conn.execute('delete from messages where rowid = ?', [msgid])

    conn.commit()
    conn.close()

def msg_thread(number):
    conn = sqlite3.connect(database)

    rowids = conn.execute(
            'select rowid from messages where recipient = ? or source = ?',
            [number, number]).fetchall()
    rowids = [rowid[0] for rowid in rowids]

    conn.close()

    for rowid in rowids:
        single_msg(rowid)
