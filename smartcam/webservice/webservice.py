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

#-------------------- Variablen --------------------
app = Flask(__name__)
HOST = '127.0.0.1' #Standard IP und Port
PORT = 80
#---------------------------- Webservice Routen ----------------------
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/bild/')
@app.route('/api/bild')
def bild():
#    d = datetime.now()
#    imgYear = "%04d" % (d.year)
#    imgMonth = "%02d" % (d.month)
#    imgDate = "%02d" % (d.day)
#    imgHour = "%02d" % (d.hour)
#    imgMins = "%02d" % (d.minute)
#    fileName = "" +str(imgYear) + str(imgMonth) + str(imgDate) + str(imgHour) + str(imgMins) + ".jpg"
#    make_picture(camera, fileName)
    return send_from_directory(directory="../images", filename="cv_bild.jpg")

@app.route('/api/config/')
@app.route('/api/config')
def config():
    f = open('../config.ini', 'r')
    content = f.read()
    f.close()
    return render_template('config.html', content=content)

@app.route('/api/')
@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/api/cable1/')
@app.route('/api/cable1')
def cable1():
    return send_from_directory(directory="../images", filename="cable1.jpg")

@app.route('/api/cablegray1/')
@app.route('/api/cablegray1')
def cablegray1():
    return send_from_directory(directory="../images", filename="cablegray1.jpg")

@app.route('/api/kreis/')
@app.route('/api/kreis')
def kreis():
    return send_from_directory(directory="../images", filename="kreis.jpg")

@app.route('/api/quadrat1/')
@app.route('/api/quadrat2')
def quadrat1():
    return send_from_directory(directory="../images", filename="quadrat1.jpg")

@app.route('/api/kreisbild/')
@app.route('/api/kreisbild')
def kreisbild():
    #return "Aktuell noch WIP"
    return render_template('kreisbild.html')

#---------------------- Main init -----------------------------
if __name__ == '__main__':
    try:
        HOST = configReader.returnEntry("web", "host")
        PORT = int(configReader.returnEntry("web", "port"))
    except Exception as e:
        logging.error("couldnt load ip from config file" + str(e))

    app.run(host=HOST, port=PORT, debug=True, threaded=True)
