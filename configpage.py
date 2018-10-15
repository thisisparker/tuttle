#!/usr/bin/env python3

import sqlite3

import dominate

from dominate.tags import *

from settings import NUMBER, database

userlist = [{'user':'useruseruser', 'number': '+12125551212'},
            {'user':'testtesttest', 'number': '+12028675309'},
           ]

def main():
    h = dominate.document()
    h.title = 'configuration'

    with h.head:
        link(rel="stylesheet", href="/style.css")
        
    body = h.add(div(id='body'))

    body.add(h1("configuration"))

    body.add(h2('notifications'))

    notification_options = body.add(table(id='notifications-table'))

    for user in userlist:
        notification_options.add(tr(td(user['user']), td(user['number']),
            td(a('❌', href="#"))))

    config_options = body.add(form(method='post', id='config-options'))

    with config_options.add(ul()):
        li(label(h2("autoresponder"), fr='autoresponder', __pretty=False),
           textarea(id="autoresponder", name="autoresponder",
                    rows=6))
        li(label(h2("authentication options"), fr='auth', __pretty=False),
            fieldset(
                input_(type='radio', id='rotate-onions', name='auth', 
                       value='rotate-onions'),
                label("Rotate Onion URLs", fr='rotate-onions'), br(),
                input_(type='radio', id='hidservauth', name='auth',
                       value='hidservauth'),
                label("Use HidServAuth authentication", fr='hidservauth')))

    config_options.add(input_(type='submit', value='Save settings', 
        id='save-button'))

    return h.render()
