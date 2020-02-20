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
#from ..configLoader import configReader
#configReader.loadConfig("config.ini")
app = Flask("WebService")

#---------------------------- Webservice Routen ----------------------
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/bild/')
@app.route('/api/bild')
def bild():
    return send_from_directory(directory="../images", filename="normal_image.jpg")

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


if __name__ == "__main__":
    # try:
    #     BIND_IP = configReader.returnEntry("web", "web_host")
    #     PORT = int(configReader.returnEntry("web", "web_port"))
    # except Exception as e:
    BIND_IP = '134.147.234.232'
    PORT = 80
    #logging.error("Could not load server ip and port from config file" + str(e))
    app.run(host=BIND_IP, port=PORT, debug=True, threaded=True)
    logging.info("Webservice started!")
