#! /usr/bin/env python

import sys
from flask import Flask
from flask import request
from flask import render_template
import sqlite3
import uuid
from collections import OrderedDict

app = Flask(__name__)

params = {
    'user': ['name'],
    'house': ['tel', 'access', 'point'],
    'voice': ['point', 'eval'],
}

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

@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        user_data = OrderedDict(
            [(p, request.form[p]) for p in params['user']]
        )
        house_data = OrderedDict(
            [(p, request.form[p]) for p in params['house']]
        )

    user_data['id'] = uuid.uuid1().__str__()
    house_data['user_id'] = user_data['id']

    save_db('user', user_data)
    save_db('house', house_data)

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

def save_db(table, data):
    conn = sqlite3.connect('db/vacant_house_travel.db')
    c = conn.cursor()
    c.execute('''REPLACE INTO {0}
    ({1}) VALUES({2})'''.format(
        table, ','.join(data.keys()), ','.join(['?'] * len(data))
    ), tuple(data.values()))
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect('db/vacant_house_travel.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS
    house(
    id INTEGER PRIMARY KEY,
    user_id NOT NULL,
    img_id,
    tel NOT NULL,
    access NOT NULL,
    point NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS
    voice(
    id INTEGER PRIMARY KEY,
    user_id NOT NULL,
    eval NOT NULL,
    point)''')
    c.execute('''CREATE TABLE IF NOT EXISTS
    user(
    id TEXT PRIMARY KEY,
    name NOT NULL,
    status
    )''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    port = int(sys.argv[1])
    init_db()
    app.run(host='0.0.0.0', port=port, debug=True)
