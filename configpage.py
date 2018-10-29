#!/usr/bin/env python3

import sqlite3

import dominate
import yaml

from readlog import add_navbar

from dominate.tags import *

from settings import NUMBER, database

def update_autoresponder(text):
    print("ok")

def main():
    h = dominate.document()
    h.title = 'configuration'

    with h.head:
        link(rel="stylesheet", href="/style.css")

    h.body = add_navbar(h.body)
        
    body = h.add(div(id='body'))

    body.add(h1("configuration"))

    body.add(h2('notifications'))

    notification_options = body.add(table(id='notifications-table'))

    try:
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
    except OSError as err:
        config = {'notifications': [], 'autoresponder': ''}

    userlist = config['notifications']
    autoresponder_text = config['autoresponder']

    for user in userlist:
        notification_options.add(tr(td(user['user']), td(user['number']),
            td(a('❌', href="#"))))

    config_options = body.add(form(method='post', id='config-options'))

    with config_options.add(ul()):
        li(label(h2("autoresponder"), fr='autoresponder', __pretty=False),
           p(strong('Current autoresponse text: '), autoresponder_text),
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
