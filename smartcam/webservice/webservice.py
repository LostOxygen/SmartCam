#!/usr/bin/python3
# -*- coding: utf8 -*-

from flask import Flask, render_template, Response, request, flash, jsonify, send_from_directory, url_for
import webbrowser
import time
from datetime import datetime
import cv2
import os
import numpy as np
from PIL import Image
import io
import configparser
from pathlib import Path
import logging
from ..configLoader import configReader
configReader.loadConfig("config.ini")

# class webService():
#     def __init__(self, bind_ip=None, port=None):
#         if bind_ip is None:
#             BIND_IP = '127.0.0.1'
#         else:
#             BIND_IP = bind_ip
#         if port is None:
#             PORT = 80
#         else:
#             PORT = port

        app = Flask("WebService")
        app.run(host=BIND_IP, port=PORT, debug=True, threaded=True)
        logging.info("Webservice started!")

#---------------------------- Webservice Routen ----------------------
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/bild/')
@app.route('/api/bild')
def bild():
    return send_from_directory(directory="../images", filename="cv_bild.jpg")

@app.route('/api/config/')
@app.route('/api/config')
def config():
    f = open('../../config.ini', 'r')
    content = f.read()
    f.close()
    return render_template('config.html', content=content)

    @app.route('/api/')
@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/api/cable/')
@app.route('/api/cable')
def cable():
    return send_from_directory(directory="../images", filename="cable.jpg")

@app.route('/api/cablegray/')
@app.route('/api/cablegray')
def cablegray():
    return send_from_directory(directory="../images", filename="cablegray.jpg")

@app.route('/api/kreis/')
@app.route('/api/kreis')
def kreis():
    return send_from_directory(directory="../images", filename="circle.jpg")

@app.route('/api/quadrat/')
def quadrat():
    return send_from_directory(directory="../images", filename="quadrat.jpg")

@app.route('/api/kreisbild/')
@app.route('/api/kreisbild')
def kreisbild():
    #return "Aktuell noch WIP"
    return render_template('kreisbild.html')

if __name__ == "__main__":
