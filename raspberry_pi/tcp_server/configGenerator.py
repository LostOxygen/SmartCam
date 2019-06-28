#!/usr/bin/python3
# -*- coding: utf8 -*-

import cv2
import sys
import os
import numpy as np
import argparse
import math
import configparser
import time
from PIL import Image
import io
from pathlib import Path
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime

# ----------------------------------- Main Code -----------------------
class Config:
    def createConfig(camera, bild_num, hoehe):
        #Variablen
        fenster_name = "OpenCV QuadratConfig"
        seitenlaenge_quadrat = 70 #in mm und standardwert
        min_threshold = 0
        max_threshold = 100
        oben_links = (400,150)
        unten_rechts = (900,600)
        kernel = np.ones((5, 5), np.uint8)
        gauss_faktor = 0
        gauss_matrix = (7,7)
        config = configparser.ConfigParser()
        maxCorners = 300 #Anzahl zu erkennenden Kanten
        qualityLevel = 0.03 #je höher desto genauer
        minDistance = 10 #mindeste Distanz zwischen Punkten

        img = camera.get_picture() #lädt frame zum erkennen

        if img is None:
            print("Fehler bei Laden des frames!" + "!\n")
            return -1

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 1)
        blur = cv2.bilateralFilter(blur, 11, 17, 17)
        blur = cv2.Canny(blur, 30, 120)

        contours, hierarchy = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #print(contours)
        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area > 400:

                approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)

                x_values = [] #Listen für x und y werte um die passenden rauszusuchen
                y_values = []

                for i in approx:

                    x_values.append(i[0][0])
                    y_values.append(i[0][1])

                upperLeft = (min(x_values), min(y_values))
                upperRight = (max(x_values), min(y_values))
                lowerLeft = (min(x_values), max(y_values))
                lowerRight = (max(x_values), max(y_values))

                edge_x1 = math.sqrt((upperLeft[0] - upperRight[0])**2 + (upperLeft[1] - upperRight[1])**2)
                edge_x2 = math.sqrt((lowerLeft[0] - lowerRight[0])**2 + (lowerLeft[1] - lowerRight[1])**2)
                edge_y1 = math.sqrt((upperLeft[0] - lowerLeft[0])**2 + (upperLeft[1] - lowerLeft[1])**2)
                edge_y2 = math.sqrt((upperRight[0] - lowerRight[0])**2 + (upperRight[1] - lowerRight[1])**2)


                cv2.drawContours(img, [approx] ,0,(0,0,255),3)
                cv2.circle(img, upperLeft, 2, (255,255,0), 2) #oben links
                cv2.circle(img, upperRight, 2, (255,255,0), 2) #oben rechts
                cv2.circle(img, lowerLeft, 2, (255,255,0), 2) #unten links
                cv2.circle(img, lowerRight, 2, (255,255,0), 2) #unten rechts

                edge_x1_mm = (seitenlaenge_quadrat / edge_x1)
                edge_x2_mm = (seitenlaenge_quadrat / edge_x2)
                edge_y1_mm = (seitenlaenge_quadrat / edge_y1)
                edge_y2_mm = (seitenlaenge_quadrat / edge_y2)

                mittelwert = (edge_x1_mm + edge_x2_mm + edge_y1_mm + edge_y2_mm) / 4
                umrechnung_mm_pro_pixel = mittelwert

                print("Quadrat erfolgreich erkannt")
                if str(bild_num) == "1":
                    config['CONFIG'] = {'host' : '192.168.8.xxx' ,
                                        'port' : '65432' ,
                                        'web_host' : '134.147.234.23x',
                                        'web_port' : '80',
                                        'AbstandZumObjekt1' : hoehe,
                                        'mm_pro_pixel1' : umrechnung_mm_pro_pixel}
                    with open('../config.ini', 'w') as configfile: #Werte in Config schreiben
                        config.write(configfile)

                elif str(bild_num) == "2":
                    if Path('../config.ini').is_file():
                        print('Config Datei gefunden')
                        config.read('../config.ini')

                        mm_pro_pixel1 = float(config['CONFIG']['mm_pro_pixel1']) #fragt Wert zum berechnen von Skalierungsfaktor ab
                        AbstandZumObjekt1 = float(config['CONFIG']['AbstandZumObjekt1'])
                        AbstandZumObjekt2 = float(hoehe)

                        skalierungsfaktor = round((mm_pro_pixel1 / umrechnung_mm_pro_pixel) / abs(AbstandZumObjekt1 - AbstandZumObjekt2), 2)

                        config['CONFIG'] = {'mm_pro_pixel2' : umrechnung_mm_pro_pixel,
                                            'AbstandZumObjekt2' : hoehe,
                                            'skalierungsfaktor_pro_mm' : skalierungsfaktor}
                        with open('../config.ini', 'w') as configfile: #Werte in Config schreiben
                            config.write(configfile)

                cv2.putText(img, "edge_x1 = " + str(edge_x1), (100,100), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)
                cv2.putText(img, "edge_y1 = " + str(edge_y1) , (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)
                cv2.putText(img, "edge_x2 = " + str(edge_x2), (100,200), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)
                cv2.putText(img, "edge_y2 = " + str(edge_y2), (100,250), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)

        #### Timestamp ####
        d = datetime.now()
        imgYear = "%04d" % (d.year)
        imgMonth = "%02d" % (d.month)
        imgDate = "%02d" % (d.day)
        imgHour = "%02d" % (d.hour)
        imgMins = "%02d" % (d.minute)
        imgSecs = "%02d" % (d.second)
        timestamp = "" + str(imgDate) + "." + str(imgMonth) + "." + str(imgYear) + " " + str(imgHour) + ":" + str(imgMins) + ":" + str(imgSecs)
        cv2.putText(img, "time = " + timestamp, (100,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)
        ####

        if str(bild_num) == "1":
            print("speichert quadrat1.jpg in /home/pi/OpenCV/raspberry_pi/bilder/")
            cv2.imwrite("../bilder/quadrat1.jpg", img) #speichert ein Bild
        elif str(bild_num) == "2":
            print("speichert quadrat2.jpg in /home/pi/OpenCV/raspberry_pi/bilder/")
            cv2.imwrite("../bilder/quadrat2.jpg", img)
        else:
            print("Wert: " + str(bild_num))
