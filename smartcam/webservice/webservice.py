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

class webService():
    def __init__(self, bind_ip=None, port=None):
        if bind_ip is None:
            self.BIND_IP = '127.0.0.1'
        else:
            self.BIND_IP = bind_ip
        if port is None:
            self.PORT = 80
        else:
            self.PORT = port

        self.app = Flask("WebService")
        self.app.run(host=self.BIND_IP, port=self.PORT, debug=True, threaded=True)
        logging.info("Webservice started!")

#---------------------------- Webservice Routen ----------------------
        @self.app.route('/index')
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/api/bild/')
        @self.app.route('/api/bild')
        def bild():
            return send_from_directory(directory="../images", filename="cv_bild.jpg")

        @self.app.route('/api/config/')
        @self.app.route('/api/config')
        def config():
            f = open('../../config.ini', 'r')
            content = f.read()
            f.close()
            return render_template('config.html', content=content)

        @self.app.route('/api/')
        @self.app.route('/api')
        def api():
            return render_template('api.html')

        @self.app.route('/api/cable/')
        @self.app.route('/api/cable')
        def cable1():
            return send_from_directory(directory="../images", filename="cable.jpg")

        @self.app.route('/api/cablegray/')
        @self.app.route('/api/cablegray')
        def cablegray1():
            return send_from_directory(directory="../images", filename="cablegray.jpg")

        @self.app.route('/api/kreis/')
        @self.app.route('/api/kreis')
        def kreis():
            return send_from_directory(directory="../images", filename="circle.jpg")

        @self.app.route('/api/quadrat/')
        def quadrat1():
            return send_from_directory(directory="../images", filename="quadrat.jpg")

        @self.app.route('/api/kreisbild/')
        @self.app.route('/api/kreisbild')
        def kreisbild():
            #return "Aktuell noch WIP"
            return render_template('kreisbild.html')
