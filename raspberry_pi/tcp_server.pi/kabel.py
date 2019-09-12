#!/usr/bin/env python3
# -*- coding: utf8 -*-

import cv2
import sys
import os
import numpy as np
import argparse
import math
import imutils
import configparser
from pathlib import Path
from pprint import pprint #Nur für Debug benötigt
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from PIL import Image
import io
from datetime import datetime

class Kabel():
    def kabel(camera, bild_num):
        #Variablen
        fenster_name = "Kabelerkenung"
        detection_size = (500, 500)
        config_test = True
        kreis_durchmesser_mm = 7
        threshold_val = 100
        threshold_max = 300
        maxCorners = 300 #Anzahl zu erkennenden Kanten
        qualityLevel = 0.03 #je höher desto genauer
        minDistance = 10 #mindeste Distanz zwischen Punkten

        # ----------- Config einlesen und überprüfen --------------------------
        config = configparser.ConfigParser()
        test = Path('../config.ini')
        if test.is_file():
            print('Config Datei gefunden')
            config.read('../config.ini')

        else:
            print('Config konnte nicht gefunden werden. Bitte erst mit configGenerator.py eine Config generieren lassen!')
            config_test = False

        durchmesser_pixel = float(config['conversion']['mm_per_pixel1']) #fragt Wert aus Config File ab

        if durchmesser_pixel == 0:
            durchmesser_pixel = 1
            print("kreis_durchmesser_pixel war 0 und wurde auf 1 gesetzt")

        umrechnung_pixel_mm = kreis_durchmesser_mm / durchmesser_pixel #Rechnet mm pro Pixel aus

        # ----------------------------------- Main Code -----------------------

        #img = camera.get_frame_cv()
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        img = rawCapture.array

        height, width = img.shape[:2] # image shape has 3 dimensions
        mittelpunkt = (int(width/2), int(height/2)) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

        rotation_mat = cv2.getRotationMatrix2D(mittelpunkt, 180, 1.)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mat[0,0])
        abs_sin = abs(rotation_mat[0,1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origo) and adding the new image center coordinates
        rotation_mat[0, 2] += bound_w/2 - mittelpunkt[0]
        rotation_mat[1, 2] += bound_h/2 - mittelpunkt[1]

        # rotate image with the new bounds and translated rotation matrix
        img = cv2.warpAffine(img, rotation_mat, (bound_w, bound_h))

        height, width = img.shape[:2]
        #mittelpunkt = (int(width/2), int(height/2))
        oben_links = (mittelpunkt[0]- detection_size[0], mittelpunkt[1]-detection_size[1]/2)
        unten_rechts = (mittelpunkt[0], mittelpunkt[1]+detection_size[1]/2)

        if img is None:
            print("Fehler bei Laden des frames!" + "!\n")
            return -1

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = gray[int(oben_links[1]) : int(unten_rechts[1]), int(oben_links[0]) : int(unten_rechts[0])]
        blur = cv2.GaussianBlur(gray, (7,7), 1)
        blur = cv2.bilateralFilter(blur, 11, 17, 17)
        blur = cv2.Canny(blur, 30, 120)

        contours = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Konturen suchen

        cv2.drawContours(gray, contours[0], -1, (0,255,0), 3)

        contours = imutils.grab_contours(contours)

        cnts = max(contours, key=cv2.contourArea)
        extLeft = tuple(cnts[cnts[:, :, 0].argmin()][0])

        corners = cv2.goodFeaturesToTrack(gray, maxCorners, qualityLevel, minDistance)
        #corners = np.int0(corners)

        min_xy = (1000,1000) #temp Var zum finden von punkt ganz oben_links
        if corners is not None:
            for i in corners:
                x,y = i.ravel()
                if x <= 1100: #zeichnet nur Relevante Punkte
                    cv2.circle(img, (x,y), 2, (0,0,255), 2)
                if x < min_xy[0]: #guckt nach kleinstem x wert
                    if x < extLeft[0]:
                        min_xy = (int(extLeft[0]), int(extLeft[1]))
                    else:
                    min_xy = (x,y)

        #berechnet Distanz von Höhe und Länge des Kabels
        dist_y = math.sqrt((min_xy[0] - min_xy[0])**2 + (min_xy[1] - mittelpunkt[1])**2)
        dist_z = math.sqrt((mittelpunkt[0] - min_xy[1])**2 + (mittelpunkt[1] - mittelpunkt[1])**2)

    #----------- optische Ausgabe --------------------------
        #Konturen zeichnen
        #cv2.drawContours(img, contours[0], -1, (0,255,0), 3)

        cv2.circle(gray, min_xy, 2, (0,255,0), 2) #zeichnet punkt ganz links
        cv2.line(img, min_xy, (min_xy[0], int(mittelpunkt[1])), (255,255,0), 2) #zeichnet linie von punkt nach oben
        #zeichnet Mittelpunkt und Linie nach links
        cv2.circle(img, mittelpunkt, 2, (255,255,0), 2)
        cv2.line(img, mittelpunkt, (min_xy[0], int(mittelpunkt[1])), (255,255,0), 2)
        cv2.line(img, mittelpunkt, min_xy, (255,255,0), 2)

        d = datetime.now()
        imgYear = "%04d" % (d.year)
        imgMonth = "%02d" % (d.month)
        imgDate = "%02d" % (d.day)
        imgHour = "%02d" % (d.hour)
        imgMins = "%02d" % (d.minute)

        #Todo Sekunde programmieren
        timestamp = "" + str(imgDate) + "." + str(imgMonth) + "." + str(imgYear) + " " + str(imgHour) + ":" + str(imgMins)
        cv2.putText(img, timestamp + " | " + "dz = " + str(round(dist_z, 2)) + " | " + "dy = " + str(round(dist_y, 2)), (20,1800), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 2, cv2.LINE_AA, 0)
    #-------------------------------------------------------
        #Umrechnung per Config in mm
        print("Distanz_Y: " + str(dist_y))
        print("umgerechnet: " + str(round(umrechnung_pixel_mm * dist_y)) + "mm")

        if str(bild_num) == "1":
            print("Speichert kabel1.jpg in /home/pi/RoboSchalt/raspberry_pi/bilder/")
            cv2.imwrite("../bilder/kabel1.jpg", img) #speichert ein Bild
        elif str(bild_num) == "2":
            print("Speichert kabel2.jpg in /home/pi/RoboSchalt/raspberry_pi/bilder/")
            cv2.imwrite("../bilder/kabel2.jpg", img)

        offset = (abs(mittelpunkt[0]), abs(mittelpunkt[1] - min_xy[1]))

        cv2.imwrite("../bilder/kabel2.jpg", gray)
        return offset
