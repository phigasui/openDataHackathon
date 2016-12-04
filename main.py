#! /usr/bin/env python

from flask import Flask
from flask import request
from flask import render_template

import sys
import sqlite3
import uuid
from collections import OrderedDict
import os
import pandas
import json

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
CLEAR_DB = '--clear-db'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

PARAMS = {
    'user': ['name'],
    'house': ['title', 'relation', 'tel', 'access', 'point'],
    'voice': ['point', 'eval'],
}

@app.route('/', methods=['GET'])
def index():
    data = pandas.read_csv('csv/東栄町基準地価平均下落.csv')
    price = json.dumps(
        tuple(zip(
            map(int, tuple(data['年'])), map(int, tuple(data['基準地価平均(円/m2)'])))
         )
    )

    return render_template('index.html', price=price)

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
            [(p, request.form[p]) for p in PARAMS['user']]
        )
        house_data = OrderedDict(
            [(p, request.form[p]) for p in PARAMS['house']]
        )

        house_data['contents'] = '/'.join(request.form['contents'])

        file = request.files['images']
        filename = str(uuid.uuid4()) + file.filename.rsplit('.', 1)[1]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        house_data['img_name'] = filename

    user_data['id'] = str(uuid.uuid1())
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
    conn = sqlite3.connect('db/vacant_house_travel.db')
    conn.row_factory = lambda c, row: {
        col[0]: row[idx] for idx, col in enumerate(c.description)
    }
    c = conn.cursor()

    c.execute('''
    SELECT id, title, img_name, access, point, contents FROM house LIMIT 20
    ''')

    houses = c.fetchall()

    return render_template('list.html', houses=houses)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
    title NOT NULL,
    relation NOT NULL,
    img_name,
    tel NOT NULL,
    access NOT NULL,
    point NOT NULL,
    contents
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

def delete_db():
    conn = sqlite3.connect('db/vacant_house_travel.db')
    c = conn.cursor()
    c.execute('''DROP TABLE house''')
    c.execute('''DROP TABLE voice''')
    c.execute('''DROP TABLE user''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    port = int(sys.argv[1])
    if CLEAR_DB in sys.argv:
        delete_db()
        sys.argv.remove(CLEAR_DB)
    init_db()
    app.run(host='0.0.0.0', port=port, debug=True)
