#!/usr/bin/python3
#-----------------
#   Jonathan Evertz
#   28.02.2019
#   Webservice für Raspberrypi / OpenCV
#-----------------


from flask import Flask, render_template, Response, request, flash, jsonify, send_from_directory, url_for
import webbrowser
from camera import VideoCamera
from kreiserkennungLive import KreisLive
#from camera_pi import Camera
from time import sleep

#from picamera.array import PiRGBArray
#from picamera import PiCamera

#-------------------- Variablen --------------------
app = Flask(__name__)
#cam = PiCamera()

#-------------------- Sonstiges --------------------
def gen(camera): #Generator für den Kamerastream
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def gen2(): #Generator für den Kreiserkennungskamerastream
    while True:
        frame = KreisLive.kreislive()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#---------------------------- Webservice Routen ----------------------
@app.route('/index', methods=['GET','POST'])
@app.route('/',  methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/api/live/')
@app.route('/api/live')
def live(): #Kamerastream in HTML einbetten
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/bild/')
@app.route('/api/bild')
def bild():
    #cam.capture('test.png')
    return render_template('bild.html')

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

@app.route('/api/kreisbild/')
@app.route('/api/kreisbild')
def kreisbild():
    return "Aktuell noch WIP"
    #return render_template('kreisbild.html')

#---------------------- Main init -----------------------------
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='80', debug=True)


#------------------ Testzeug -----------------------------
#if request.method == 'POST':
#    if request.form['submit_button'] == '1':
#        return send_from_directory(directory="static", filename="test.png")
#    else:
#        return "Datei nicht gefunden!"
#elif request.method == 'GET':
#    return render_template('index.html')
#----------------------------------------------------------
