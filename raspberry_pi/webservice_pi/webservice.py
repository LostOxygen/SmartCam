#!/usr/bin/python3 -----------------
#   Jonathan Evertz
#   18.03.2019
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

#-------------------- Variablen --------------------
app = Flask(__name__)
#-------------------- Sonstiges --------------------
def gen(camera): #Generator für den Kamerastream
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def make_picture(camera):
    d = datetime.now()
    imgYear = "%04d" % (d.year)
    imgMonth = "%02d" % (d.month)
    imgDate = "%02d" % (d.day)
    imgHour = "%02d" % (d.hour)
    imgMins = "%02d" % (d.minute)
    fileName = "" +str(imgYear) + str(imgMonth) + str(imgDate) + str(imgHour) + str(imgMins) + ".jpg"
    bild = open(fileName, "w")
    #bild.write(camera.get_frame())
    bild.close()

    img = Image.open(fileName)
    img.save(camera.get_frame())

#def gen2(): #Generator für den Kreiserkennungskamerastream
#    while True:
#        frame = KreisLive.kreislive(cam)
#        yield (b'--frame\r\n'
#               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#---------------------------- Webservice Routen ----------------------
@app.route('/index', methods=['GET','POST'])
@app.route('/',  methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/api/live/')
@app.route('/api/live')
def live(): #Kamerastream in HTML einbetten
    return Response(gen(Camera()),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/bild/')
@app.route('/api/bild')
def bild():
    make_picture(Camera())
    #return "Hier wird bald Bild: " + fileName + " sein."
    return send_from_directory(directory="", filename=fileName)

@app.route('/api/offset/')
@app.route('/api/offset')
def offset():
    return render_template('offset.html')

@app.route('/api/')
@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/api/kreislive/')
@app.route('/api/kreislive')
def kreislive():
    return Response(gen2(), mimetype='multipart/x-mixed-replace; boundary=frame')
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
