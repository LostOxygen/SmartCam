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
from picamera.array import PiRGBArray
from picamera import PiCamera

# ----------------------------------- Main Code -----------------------
class Config:
    def createConfig(camera, bild_num):
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

        img = camera.get_frame_cv() #lädt frame zum erkennen

        if img is None:
            print("Fehler bei Laden des frames!" + "!\n")
            return -1

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 1)
        blur = cv2.bilateralFilter(blur, 11, 17, 17)
        blur = cv2.Canny(blur, 30, 120)

        contours, hierarchy = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(type(contours))
        for cnt in contours:
            print("test1")
            area = cv2.contourArea(cnt)
            print("test2")
            approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
            print("test3")
            x_values = [] #Listen für x und y werte um die passenden rauszusuchen
            y_values = []
            print("test5")
            for i in approx:
                x_values.append(i[0][0])
                y_values.append(i[0][1])

            if area > 400:
                print("test4")
                cv2.drawContours(img, [approx] ,0,(0,0,255),3)
                cv2.circle(img, (min(x_values), min(y_values)), 2, (255,255,0), 2) #oben links
                cv2.circle(img, (max(x_values), min(y_values)), 2, (255,255,0), 2) #oben rechts
                cv2.circle(img, (min(x_values), max(y_values)), 2, (255,255,0), 2) #unten links
                cv2.circle(img, (max(x_values), max(y_values)), 2, (255,255,0), 2) #unten rechts

                x_seite = math.sqrt((min(x_values) - max(x_values))**2 + (min(y_values) - min(y_values))**2)
                y_seite = math.sqrt((min(x_values) - min(x_values))**2 + (min(y_values) - max(y_values))**2)

                umrechnung_mm_pro_pixel = round(seitenlaenge_quadrat / x_seite, 2)

                if bild_num == 1:
                    print("test1")
                    config['CONFIG'] = {'host' : '192.168.8.xxx' ,
                                        'port' : '65432' ,
                                        'web_host' : '134.147.234.23x',
                                        'web_port' : '80',
                                        'AbstandZumObjekt1' : '15',
                                        'AbstandZumObjekt2' : '20',
                                        'mm_pro_pixel1' : umrechnung_mm_pro_pixel}
                    with open('../config.ini', 'w') as configfile: #Werte in Config schreiben
                        config.write(configfile)
                elif bild_num == 2:
                    print("test2")
                    if Path('../config.ini').is_file():
                        print('Config Datei gefunden')
                        config.read('../config.ini')

                        mm_pro_pixel1 = float(config['CONFIG']['mm_pro_pixel1']) #fragt Wert zum berechnen von Skalierungsfaktor ab
                        AbstandZumObjekt1 = float(config['CONFIG']['AbstandZumObjekt1'])
                        AbstandZumObjekt2 = float(config['CONFIG']['AbstandZumObjekt2'])

                        skalierungsfaktor = round((mm_pro_pixel1 / umrechnung_mm_pro_pixel) / abs(AbstandZumObjekt1 - AbstandZumObjekt2), 2)

                        config['CONFIG'] = {'mm_pro_pixel2' : umrechnung_mm_pro_pixel,
                                            'skalierungsfaktor_pro_cm' : skalierungsfaktor}
                        with open('../config.ini', 'w') as configfile: #Werte in Config schreiben
                            config.write(configfile)
                print("test3")
                cv2.putText(img, str(round(x_seite, 2)) + "px X_Seite" , (100,100), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)
                cv2.putText(img, str(round(y_seite, 2)) + "px Y_Seite" , (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)

        if bild_num == 1:
            print("speichert quadrat1.jpg")
            cv2.imwrite("../bilder/quadrat1.jpg", img) #speichert ein Bild
        elif bild_num == 2:
            print("speichert quadrat1.jpg")
            cv2.imwrite("../bilder/quadrat2.jpg", img)
