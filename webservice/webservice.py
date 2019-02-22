#!/usr/bin/python3

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test')
def test():
    return 'test uff!'

if __name__ == '__main__':
    app.run()
