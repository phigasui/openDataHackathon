#! /usr/bin/env python

import sys
from flask import Flask
from flask import request
from flask import render_template
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/input', methods=['GET'])
def input():
    return render_template('input.html')

@app.route('/input_voice', methods=['GET'])
def input_voice():
    return render_template('input_voice.html')

@app.route('/input_admin', methods=['GET'])
def input_admin():
    return render_template('input_admin.html')

@app.route('/complete', methods=['POST'])
def save():
    return render_template('complete.html')

@app.route('/complete_voice', methods=['POST'])
def save_voice():
    return render_template('complete_voice.html')

@app.route('/complete_admin', methods=['POST'])
def save_admin():
    return render_template('complete_admin.html')

@app.route('/list', methods=['GET'])
def list():
    return render_template('list.html')

def init_db():
    conn = sqlite3.connect('db/vacant_house_travel.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS
    house(id, user_id, img_id, point, content)''')
    c.execute('''CREATE TABLE IF NOT EXISTS
    voice(id TEXT, user_id, point, eval)''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    port = int(sys.argv[1])
    init_db()
    app.run(host='0.0.0.0', port=port, debug=True)
