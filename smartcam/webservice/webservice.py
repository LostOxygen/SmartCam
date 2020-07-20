#!/usr/bin/python3
# -*- coding: utf8 -*-

from flask import Flask, render_template, Response, request, flash, jsonify, send_from_directory, url_for
import webbrowser
import time
import datetime
import platform
import subprocess
import cv2
import os
import numpy as np
from PIL import Image
import io
from pathlib import Path
import logging

from webConfigLoader import configReader
configReader.loadConfig("/home/pi/.smartcam/config.ini")
image_path = configReader.returnEntry('options', 'imagepath')

app = Flask("SmartCam Webservice")

'''
Flask implementation of a webservice. Mainly registers all the necessary routes to the pages which are located in the 'templates' folder.
The 'static' folder holds javascript and css libraries so their imports don't rely on CDN services.
'''

#---------------------------- Webservice Routen ----------------------
@app.route('/index')
@app.route('/')
def index():
    # loads the configReader values to check if a module is loaded and then displays their debug images
    circle = str(configReader.returnEntry("modules", "circle"))
    cable = str(configReader.returnEntry("modules", "cable"))
    parts = str(configReader.returnEntry("modules", "parts"))
    led = str(configReader.returnEntry("modules", "led"))
    iolink = str(configReader.returnEntry("modules", "iolink"))
    schunk = str(configReader.returnEntry("modules", "schunk"))
    return render_template('index.html', circle=circle, cable=cable, parts=parts, led=led, iolink=iolink, schunk=schunk)

@app.route('/system')
@app.route('/system/')
def stats():
    # displays the system status
    today = datetime.date.today()
    system = platform.system()
    node = platform.node()
    arch = platform.machine()
    user = "pi"

    get_uptime = subprocess.Popen('uptime', stdout=subprocess.PIPE)
    uptime = get_uptime.stdout.read()

    return render_template('system.html', today=today, system=system, node=node, arch=arch, user=user, uptime=uptime)

@app.route('/api/')
@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/api/config/')
@app.route('/api/config')
def config():
    # loads the config file as a raw file to display
    f = open('/home/pi/.smartcam/config.ini', 'r')
    content = f.read()
    f.close()
    return render_template('config.html', content=content)

@app.route('/api/bild/')
@app.route('/api/bild')
def bild():
    return send_from_directory(directory=image_path, filename="normal_image.jpg")

@app.route('/api/cable/')
@app.route('/api/cable')
def cable():
    return send_from_directory(directory=image_path, filename="cable1.jpg")

@app.route('/api/cablegray/')
@app.route('/api/cablegray')
def cablegray():
    return send_from_directory(directory=image_path, filename="cablegray1.jpg")

@app.route('/api/cable2/')
@app.route('/api/cable2')
def cable2():
    return send_from_directory(directory=image_path, filename="cable2.jpg")

@app.route('/api/cablegray1/')
@app.route('/api/cablegray1')
def cablegray2():
    return send_from_directory(directory=image_path, filename="cablegray2.jpg")

@app.route('/api/kreis/')
@app.route('/api/kreis')
def kreis():
    return send_from_directory(directory=image_path, filename="circle.jpg")

@app.route('/api/quadrat/')
@app.route('/api/quadrat')
def quadrat():
    return send_from_directory(directory=image_path, filename="quadrat.jpg")

@app.route('/modules/')
@app.route('/modules')
def modules():
    # lists all the build in modules and their status
    circle = str(configReader.returnEntry("modules", "circle"))
    cable = str(configReader.returnEntry("modules", "cable"))
    parts = str(configReader.returnEntry("modules", "parts"))
    led = str(configReader.returnEntry("modules", "led"))
    iolink = str(configReader.returnEntry("modules", "iolink"))
    schunk = str(configReader.returnEntry("modules", "schunk"))
    return render_template('modules.html', circle=circle, cable=cable, parts=parts, led=led, iolink=iolink, schunk=schunk)


@app.route('/send_image/<filename>')
def send_image(filename):
    return send_from_directory(directory=image_path, filename=filename)

@app.route('/reboot_call')
def reboot():
    try:
        os.system("sudo systemctl reboot -i")
    except Exception as e:
        logging.error("Could't reboot system: " + str(e))

@app.route('/update_call')
def update():
    try:
        os.system("git pull")
    except Exception as e:
        logging.error("Could't update system: " + str(e))


if __name__ == "__main__":
    BIND_IP = '0.0.0.0'
    PORT = 80

    app.run(host=BIND_IP, port=PORT, debug=True, threaded=True)
    logging.info("Webservice started!")
