#! /usr/bin/env python3

import readlog
import sendmsg

from flask import Flask, request, send_from_directory

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        message = request.form.get('message')

        sendmsg.send(recipient, message)

    return readlog.main() 

@app.route('/style.css')
def serve_style():
    return app.send_static_file('style.css')

@app.route('/attachments/<path:filename>')
def serve_attachments(filename):
    return send_from_directory('static/attachments', filename)
