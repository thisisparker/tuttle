#!/bin/env python3

import sqlite3

from settings import database

def single_msg(msgid):
    conn = sqlite3.connect(database)

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
