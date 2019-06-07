#!/usr/bin/python3
# -*- coding: utf8 -*-

import cv2
import sys
import os
import numpy as np
import argparse
import math
import configparser
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from PIL import Image
import io
from datetime import datetime

from camera_pi import Camera

class Config():
    def createConfig(camera = Camera(), bildnum):
        #Variablen
        kreis_durchmesser_mm = 7
        min_threshold = 0
        max_threshold = 100
        gauss_faktor = 0
        gauss_matrix = (7,7)
        config = configparser.ConfigParser()
        maxCorners = 300 #Anzahl zu erkennenden Kanten
        qualityLevel = 0.03 #je höher desto genauer
        minDistance = 10 #mindeste Distanz zwischen Punkten

        # ----------------------------------- Main Code -----------------------
        img = camera.get_frame_cv()

        if img is None:
            print("Fehler bei Laden des frames!" + "!\n")
            return -1

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 1)
        blur = cv2.bilateralFilter(blur, 11, 17, 17)
        blur = cv2.Canny(blur, 30, 120)

        contours, hierarchy = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rect = cv2.minAreaRect(contours)

        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img, [box] ,0,(0,0,255),2)


        config['CONFIG'] = {'post' : '192.168.8.xxx' , 'port' : '65432' , 'AbstandZumObjekt' : '15', 'DurchmesserKreisInPixel' : kkreis_r}
        with open('../config.ini', 'w') as configfile: #Werte in Config schreiben
            config.write(configfile)
        return True
