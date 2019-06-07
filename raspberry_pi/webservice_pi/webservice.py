#!/usr/bin/python3
# -*- coding: utf8 -*-

from flask import Flask, render_template, Response, request, flash, jsonify, send_from_directory, url_for
import webbrowser
from camera import VideoCamera
from kreiserkennungLive import KreisLive
from camera_pi import Camera
import time
from datetime import datetime
import cv2
import os
import numpy as np
from PIL import Image
import io
import configparser
from pathlib import Path

#-------------------- Variablen --------------------
app = Flask(__name__)
camera = Camera()
HOST = '127.0.0.1' #Standard IP und Port
PORT = 80
config_test = True
#-------------------- Sonstiges --------------------

def gen(camera): #Generator für den Kamerastream
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def make_picture(camera, fileName):
    if camera.get_frame is not None:
        img2 = Image.open(io.BytesIO(camera.get_frame())) #lädt frame als ByteIO um es zu öffnen
        img2.save("../bilder/" + fileName) #speichert es als fileName ab
    else:
        return "Kamera Frame ist None"

def gen_kreis(camera): #Generator für den Kreiserkennungskamerastream
    while True:
        frame = KreisLive.kreislive(camera.get_frame())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#---------------------------- Webservice Routen ----------------------
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/live/')
@app.route('/api/live')
def live(): #Kamerastream in HTML einbetten
    return Response(gen(camera),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/bild/')
@app.route('/api/bild')
def bild():
    #camera = Camera()
    d = datetime.now()
    imgYear = "%04d" % (d.year)
    imgMonth = "%02d" % (d.month)
    imgDate = "%02d" % (d.day)
    imgHour = "%02d" % (d.hour)
    imgMins = "%02d" % (d.minute)
    fileName = "" +str(imgYear) + str(imgMonth) + str(imgDate) + str(imgHour) + str(imgMins) + ".jpg"
    make_picture(camera, fileName)
    #del camera
    return send_from_directory(directory="images", filename=fileName)

@app.route('/api/config/')
@app.route('/api/config')
def offset():
    return render_template('config.html')

@app.route('/api/')
@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/api/kabel1/')
@app.route('/api/kabel1')
def kabel1():
    return send_from_directory(directory="../bilder", filename="kabel1.jpg")

@app.route('/api/kabel2/')
@app.route('/api/kabel2')
def kabel2():
    return send_from_directory(directory="../bilder", filename="kabel2.jpg")

@app.route('/api/kreis/')
@app.route('/api/kreis')
def kreis():
    return send_from_directory(directory="../bilder", filename="kreis.jpg")

@app.route('/api/quadrat1/')
@app.route('/api/quadrat2')
def kreis():
    return send_from_directory(directory="../bilder", filename="quadrat1.jpg")

@app.route('/api/quadrat2/')
@app.route('/api/quadrat2')
def kreis():
    return send_from_directory(directory="../bilder", filename="quadrat2.jpg")

@app.route('/api/kreislive/')
@app.route('/api/kreislive')
def kreislive():
    return Response(gen_kreis(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/kreisbild/')
@app.route('/api/kreisbild')
def kreisbild():
    #return "Aktuell noch WIP"
    return render_template('kreisbild.html')

#---------------------- Main init -----------------------------
if __name__ == '__main__':

    config = configparser.ConfigParser()
    test = Path('../config.ini')
    if test.is_file():
        print('Config Datei gefunden')
        config.read('../config.ini')

    else:
        print('Config konnte nicht gefunden werden. Bitte erst mit configGenerator.py eine Config generieren lassen!')
        config_test = False

    if config_test:
        HOST = config['CONFIG']['web_host']
        PORT = int(config['CONFIG']['web_port'])

    app.run(host=HOST, port=PORT, debug=True, threaded=True)
