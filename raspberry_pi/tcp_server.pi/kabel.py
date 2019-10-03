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
    #Variablen
    fenster_name = "Kabelerkenung"
    detection_size = (500, 500)
    config_test = True
    umrechnung_pixel_mm = 1 #to avoid errors the value is preset to 1
    maxCorners = 300 #Anzahl zu erkennenden Kanten
    qualityLevel = 0.03 #je höher desto genauer
    minDistance = 10 #mindeste Distanz zwischen Punkten

    def visualization_rgb(img, min_xy, height, mittelpunkt):
    #visualization of the rgb picture
        cv2.circle(img, min_xy, 4, (255, 255, 255), 4) #zeichnet punkt ganz links
        cv2.line(img, min_xy, (min_xy[0], int(height/2)), (255,255,255), 2) #zeichnet linie von punkt nach oben
        #zeichnet Mittelpunkt und Linie nach links
        cv2.circle(img, mittelpunkt, 2, (255,255,255), 2)
        cv2.line(img, mittelpunkt, (min_xy[0], int(height/2)), (255,255,255), 2)
        cv2.line(img, mittelpunkt, min_xy, (255,255,255), 2)
        d = datetime.now()
        imgYear = "%04d" % (d.year)
        imgMonth = "%02d" % (d.month)
        imgDate = "%02d" % (d.day)
        imgHour = "%02d" % (d.hour)
        imgMins = "%02d" % (d.minute)
        timestamp = "" + str(imgDate) + "." + str(imgMonth) + "." + str(imgYear) + " " + str(imgHour) + ":" + str(imgMins)
        cv2.putText(img, timestamp + " | " + str(round(dist_x_mm, 2)) + " mm | " + str(round(dist_y_mm, 2)) + " mm ", (20,1060), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 2, cv2.LINE_AA, 0)

        print("Distanz_Y: " + str(dist_y))
        print("umgerechnet: " + str(round(dist_y_mm, 2)) + "mm")

    def visualization_gray(gray, extLeft, g_heihgt, g_mittelpunkt):
        cv2.circle(gray, extLeft, 4, (255, 255, 255), 4) #zeichnet punkt ganz links
        cv2.line(gray, extLeft, (extLeft[0], int(g_height/2)), (255,255,255), 2) #zeichnet linie von punkt nach oben
        #zeichnet Mittelpunkt und Linie nach links
        cv2.circle(gray, g_mittelpunkt, 2, (255,255,255), 2)
        cv2.line(gray, g_mittelpunkt, (extLeft[0], int(g_height/2)), (255,255,255), 2)
        cv2.line(gray, g_mittelpunkt, extLeft, (255,255,255), 2)

    def saveImg(bild_num, img, gray):
        if str(bild_num) == "1":
            print("Speichert kabel1.jpg und kabelgrau1.jpg in /home/pi/RoboSchalt/raspberry_pi/bilder/")
            cv2.imwrite("../bilder/kabelgrau1.jpg", gray)
            cv2.imwrite("../bilder/kabel1.jpg", img) #speichert ein Bild
        elif str(bild_num) == "2":
            print("Speichert kabel2.jpg und kabelgrau2.jpg in /home/pi/RoboSchalt/raspberry_pi/bilder/")
            cv2.imwrite("../bilder/kabelgrau2.jpg", gray)
            cv2.imwrite("../bilder/kabel2.jpg", img)

    def config():
        # ----------- reads config and checks values --------------------------
        config = configparser.ConfigParser()
        test = Path('../config.ini')
        if test.is_file():
            print('Config Datei gefunden')
            config.read('../config.ini')

        else:
            print('Config konnte nicht gefunden werden. Bitte erst mit configGenerator.py eine Config generieren lassen!')
            Kabel.config_test = False

        Kabel.umrechnung_pixel_mm = float(config['conversion']['mm_per_pixel1']) #fragt Wert aus Config File ab

    def rotate(img, mittelpunkt, width, height):
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
        return img

    def kabel(camera, bild_num):
        #main part which checks for wires and their angle
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        img = rawCapture.array

        height, width = img.shape[:2] # image shape has 3 dimensions
        mittelpunkt = (int(width/2), int(height/2)) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape
        img = Kabel.rotate(img, mittelpunkt, width, height)  #rotiert das Bild ggf.
        height, width = img.shape[:2]

        oben_links = (int(mittelpunkt[0]- Kabel.detection_size[0]), int(mittelpunkt[1]- Kabel.detection_size[1]/2))
        unten_rechts = (int(mittelpunkt[0]), int(mittelpunkt[1]+ Kabel.detection_size[1]/2))

        if img is None: #to prevent errors with empty images
            print("Fehler bei Laden des frames!" + "!\n")
            return -1

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = gray[int(oben_links[1]) : int(unten_rechts[1]), int(oben_links[0]) : int(unten_rechts[0])] #schneidet graubild auf relevanten Bereich zu
        blur = cv2.GaussianBlur(gray, (7,7), 1)
        blur = cv2.bilateralFilter(blur, 11, 17, 17)
        blur = cv2.Canny(blur, 30, 120)

        contours = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Konturen suchen
        corners = cv2.goodFeaturesToTrack(gray, Kabel.maxCorners, Kabel.qualityLevel, Kabel.minDistance)
        cv2.drawContours(gray, contours[0], -1, (0,255,0), 3)

        contours = imutils.grab_contours(contours)
        cnts = max(contours, key=cv2.contourArea)
        extLeft = tuple(cnts[cnts[:, :, 0].argmin()][0])

        g_height, g_width = gray.shape[:2]
        g_mittelpunkt = (g_width, int(g_height/2))
        Kabel.visualization_gray(gray, extLeft, g_height, g_mittelpunkt)

        min_xy = extLeft #temp Var zum finden von punkt ganz oben_links
        if corners is not None:
            for i in corners:
                x,y = i.ravel()
                if x <= 1100: #zeichnet nur Relevante Punkte
                    cv2.circle(img, (x,y), 2, (0,0,255), 2)
                if x < min_xy[0]: #guckt nach kleinstem x wert
                    min_xy = (x,y)

        dist_y = g_mittelpunkt[1] - min_xy[1]
        dist_x = g_mittelpunkt[0] - min_xy[0]
        min_xy = (int(mittelpunkt[0] - dist_x), int(mittelpunkt[1] - dist_y)) #rechnet min_xy auf das gesamte Bild um
        dist_y_mm = (dist_y * Kabel.umrechnung_pixel_mm)/2
        dist_x_mm = (dist_x * Kabel.umrechnung_pixel_mm)/2

        Kabel.visualization_rgb(img, min_xy, height, mittelpunkt)

        Kabel.saveImg(bild_num, img, gray)
        offset = (round(dist_x_mm, 2), round(dist_y_mm, 2))

        return offset
