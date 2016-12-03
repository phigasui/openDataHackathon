#! /usr/bin/env python

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/input', methods=['GET'])
def input():
    return render_template('input_form.html')

@app.route('/save', methods=['POST'])
def save():
    return render_template('complete.html')

@app.route('/list', methods=['GET'])
def list():
    return render_template('list.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
