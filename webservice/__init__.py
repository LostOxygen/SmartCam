#!/usr/bin/python3

import os

from flask import Flask

def create_app(test_config=None):
    #Applikation und Config wird erstellt
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev', DATABSE=os.path.join(app.instance_path, 'flaskr.sqlite'))
    #Secret Key sollte in Config überschrieben werden, Database wird im Instanzordner gespeichert
    if test_config is None:
        #Instanzconfig laden
        app.config.from_pyfile('config.py', silent=True)
    else:
        #testconfig laden, falls sie der funktion übergeben wurde
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Ich sage hier nur Hallo!'

    return app
