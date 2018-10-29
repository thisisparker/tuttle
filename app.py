#! /usr/bin/env python3

import configpage
import readlog
import sendmsg
import deletemsg

import sqlite3

from flask import Flask, redirect, request, send_from_directory, url_for

from settings import database

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def serve_home():
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        message = request.form.get('message')
        msg_to_delete = request.form.get('delete-msg')
        thread_to_delete = request.form.get('delete-thread')

        if recipient and message:
            msg = sendmsg.send(recipient, message)
            conn = sqlite3.connect(database)
            msg.log_to_db(conn)
            print("- logging reply to db")
            conn.commit()

        if msg_to_delete:
            deletemsg.single_msg(msg_to_delete)

        if thread_to_delete:
            deletemsg.msg_thread(thread_to_delete)

        return redirect(url_for("serve_home"))

    return readlog.main() 

@app.route('/config', methods=['GET', 'POST'])
def serve_config():
    if request.method == 'POST':
        autoresponder = request.form.get('autoresponder')
        hidservauth = request.form.get('hidservauth')
        rotateonions = request.form.get('rotate-onions')

        if autoresponder:
            configpage.update_autoresponder(autoresponder)

        return redirect(url_for("serve_config"))

    return configpage.main()

@app.route('/style.css')
def serve_style():
    return app.send_static_file('style.css')

@app.route('/attachments/<path:filename>')
def serve_attachments(filename):
    return send_from_directory('static/attachments', filename)
