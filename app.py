#! /usr/bin/env python3

import configpage
import readlog
import sendmsg

from flask import Flask, request, send_from_directory

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def serve_home():
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        message = request.form.get('message')

        sendmsg.send(recipient, message)

    return readlog.main() 

@app.route('/config', methods=['GET', 'POST'])
def serve_config():
    return configpage.main()

@app.route('/style.css')
def serve_style():
    return app.send_static_file('style.css')

@app.route('/attachments/<path:filename>')
def serve_attachments(filename):
    return send_from_directory('static/attachments', filename)
