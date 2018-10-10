#!/usr/bin/env python3

import sqlite3

import dominate

from dominate.tags import *

from settings import NUMBER, database

def main():
    h = dominate.document()
    h.title = 'configuration'

    with h.head:
        link(rel="stylesheet", href="/style.css")
        
    body = h.add(div(id='body'))

    body.add(h1("configuration"))

    return h.render()
