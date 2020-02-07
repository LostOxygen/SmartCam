#!/usr/bin/python3
# -*- coding: utf8 -*-

import logging
import cv2
import sys
import os
import numpy as np
import argparse
import math
from ..configLoader import configReader
from pathlib import Path
from pprint import pprint #Nur für Debug benötigt
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from PIL import Image
import io
from datetime import datetime

class circleDetection():
    def __init__(cls):
        pass

    @classmethod
    def detectCircles(cls, picture): #Picture ist bool und ist für das erstellen eines Bildes oder nicht

        #Variablen
        image_frame = None
        offset = (0,0)
        config_test = True
        kreis_durchmesser_mm = 7
        min_threshold = 0
        max_threshold = 100
        oben_links = (460,144)
        unten_rechts = (1360,1044)
        fenster_name = "Circle Detection"
        gauss_faktor = 0
        gauss_matrix = (7,7)
        clear = lambda: os.system('clear')
        #dateinamen generieren
        d = datetime.now()
        imgYear = "%04d" % (d.year)
        imgMonth = "%02d" % (d.month)
        imgDate = "%02d" % (d.day)
        imgHour = "%02d" % (d.hour)
        imgMins = "%02d" % (d.minute)
        fileName = "" +str(imgYear) + str(imgMonth) + str(imgDate) + str(imgHour) + str(imgMins) + ".jpg"

        # ----------- Config einlesen und überprüfen --------------------------
        umrechnung_pixel_mm = float(configReader.returnEntry('conversion', 'mm_per_pixel1')) #fragt Wert aus Config File ab

        if umrechnung_pixel_mm == 0:
            umrechnung_pixel_mm = 1
            logging.info("set circle diameter to 1 instead of 0!")

        upperLeft = (460, 144)
        upperRight = (1360, 144)
        lowerLeft = (460, 1044)
        lowerRight = (1360, 1044)

        middle = (upperLeft[0] + 0.5*(upperRight[0]-upperLeft[0]), upperLeft[1] + 0.5*(lowerRight[1]-upperLeft[1]))

        oben_links = (int(middle[0] - 450) , int(middle[1] - 450))
        unten_rechts = (int(middle[0] + 450) , int(middle[1] + 450))

        # ----------------------------------- Main Code -----------------------
        camera = PiCamera()
        camera.resolution = (1920, 1080)
        camera.hflip = True
        camera.vflip = True

        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        frame = rawCapture.array

        # in Graubild umwandeln
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #blurren
        blur = cv2.medianBlur(gray, 5)
        #zeichnet Rechteckt
        rechteck = cv2.rectangle(frame, oben_links, unten_rechts, (100,50,200), 5)

        cv2.putText(frame, str(oben_links) , oben_links, cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_AA, 0)
        cv2.putText(frame, str(unten_rechts) , unten_rechts, cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_AA, 0)
        cv2.putText(frame, str((oben_links[0], unten_rechts[1])) , (oben_links[0], unten_rechts[1]), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_AA, 0)
        cv2.putText(frame, str((unten_rechts[0], oben_links[1])) , (unten_rechts[0], oben_links[1]), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_AA, 0)

        #Temp Variablen zum arbeiten für nächsten Kreis
        kdistanz = 100000
        kkreis_r = 0
        kkreis_xy = (0,0)

        #verarbeitet den Teil im Rechteck
        ausschnitt = blur[oben_links[1] : unten_rechts[1], oben_links[0] : unten_rechts[0]]
        mittelpunkt = (int(oben_links[0]+(unten_rechts[0]-oben_links[0])/2), int(oben_links[1]+(unten_rechts[1]-oben_links[1])/2))

        cv2.circle(ausschnitt,mittelpunkt,2,(0,0,255),3) #zeichnet Mittelpunkt
        #minRadius=27 maxRadius=32
        #circles = cv2.HoughCircles(ausschnitt,cv2.HOUGH_GRADIENT,1,20,param1=100,param2=20,minRadius=25,maxRadius= 50)
        circles = cv2.HoughCircles(ausschnitt,cv2.HOUGH_GRADIENT,1,20,param1=100,param2=20,minRadius=15,maxRadius= 30)
        if circles is not None:
            logging.info("found circles!")
            for i in circles[0,:]:
        		#Kreis zeichnen
                cv2.circle(frame,(int(oben_links[0] + i[0]), int(oben_links[1] + i[1])),i[2],(0,0,255),2) #(Quelle, (x,y) = Center, Radius, Farbe, )
                #Mittelpunkt malen
                cv2.circle(frame,(int(oben_links[0] + i[0]), int(oben_links[1] + i[1])),2,(0,0,255),3)
                #den nächsten Kreis finden

                distanz = math.sqrt(((mittelpunkt[0] - (oben_links[0]+i[0]))**2) + ((mittelpunkt[1] - (oben_links[1]+i[1]))**2))

                if distanz < kdistanz:
                    kdistanz = distanz
                    kkreis_r = i[2]
                    kkreis_xy = (int(oben_links[0] + i[0]), int(oben_links[1] + i[1]))

        ausschnitt = cv2.cvtColor(ausschnitt, cv2.COLOR_GRAY2RGB)
        cv2.circle(frame, mittelpunkt, 2, (255,255,255),2) #Mittelpunkt des Bildes
        cv2.circle(frame, kkreis_xy, kkreis_r,(0,255,0),2) #ausgewählter Kreisen
        cv2.circle(frame, kkreis_xy, 2,(0,255,0),2) #Mittelpunkt des Kreises

        #### Timestamp ####
        d = datetime.now()
        imgYear = "%04d" % (d.year)
        imgMonth = "%02d" % (d.month)
        imgDate = "%02d" % (d.day)
        imgHour = "%02d" % (d.hour)
        imgMins = "%02d" % (d.minute)
        #Todo Sekunde programmieren
        timestamp = "" + str(imgDate) + "." + str(imgMonth) + "." + str(imgYear) + " " + str(imgHour) + ":" + str(imgMins)

        if circles is not None: #Damit nur eine Linie gezeichnet wird, wenn er Kreise findet
            offset = (mittelpunkt[0] - kkreis_xy[0] , mittelpunkt[1] - kkreis_xy[1])
            offset = (round((offset[0]*umrechnung_pixel_mm),2), round((offset[1]*umrechnung_pixel_mm),2))

            cv2.line(frame,mittelpunkt,kkreis_xy,(255,255,255),5) #Linie zwischen Mittelpunkt und ausgewähltem Kreis

            #cv2.putText(frame, str(round(kdistanz, 2)) , kkreis_xy, cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 2, cv2.LINE_AA, 0)

            cv2.putText(frame, timestamp + " | " + str(offset[0]) + " mm " + " | " + str(offset[1]) + " mm " + " | " + str(round((kdistanz*umrechnung_pixel_mm),2)) + " mm ", (20,1060), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 2, cv2.LINE_AA, 0)

        else:
            offset = (999999,999999)

        image_frame = frame

        if picture:
            if image_frame is not None:
                cv2.imwrite("../images/" + fileName, image_frame) #speichert es als fileName ab
                logging.info("saving image: " + fileName + " in: ../images/")
                del camera
                return True
        else:
            cv2.imwrite("../images/circle.jpg", frame) #speichert ein Bild
            del camera
            return offset
