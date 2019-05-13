#!/usr/bin/python3 -----------------
#   Jonathan Evertz
#   19.03.2019
#   Webservice für Raspberrypi / OpenCV
#-----------------

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

#-------------------- Variablen --------------------
app = Flask(__name__)
camera = Camera()
#-------------------- Sonstiges --------------------

def gen(camera): #Generator für den Kamerastream
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def make_picture(camera, fileName):
    if camera.get_frame is not None:
        img2 = Image.open(io.BytesIO(camera.get_frame())) #lädt frame als ByteIO um es zu öffnen
        img2.save("/home/pi/Desktop/OpenCV/raspberry_pi/webservice_pi/images/" + fileName) #speichert es als fileName ab
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

@app.route('/api/offset/')
@app.route('/api/offset')
def offset():
    return render_template('offset.html')

@app.route('/api/')
@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/api/kabel/')
@app.route('/api/kabel')
def api():
    return send_from_directory(directory="/home/pi/Desktop/OpenCV/raspberry_pi/bilder", filename="kabel.jpg")

@app.route('/api/kreis/')
@app.route('/api/kreis')
def api():
    return send_from_directory(directory="/home/pi/Desktop/OpenCV/raspberry_pi/bilder", filename="kreis.jpg")

@app.route('/api/kreislive/')
@app.route('/api/kreislive')
def kreislive():
    return Response(gen_kreis(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
#     return "Aktuell noch WIP"
@app.route('/api/kreisbild/')
@app.route('/api/kreisbild')
def kreisbild():
    #return "Aktuell noch WIP"
    return render_template('kreisbild.html')

#---------------------- Main init -----------------------------
if __name__ == '__main__':
    app.run(host='134.147.234.230', port=80, debug=True, threaded=True)


#------------------ Testzeug -----------------------------
#if request.method == 'POST':
#    if request.form['submit_button'] == '1':
#        return send_from_directory(directory="static", filename="test.png")
#    else:
#        return "Datei nicht gefunden!"
#elif request.method == 'GET':
#    return render_template('index.html')
#----------------------------------------------------------
