#!/usr/bin/python3

##########################
# Author: Jonathan Evertz
# Date: 21.2.2019
# Version: 1.2
#
##########################

import cv2
import sys
import os
import numpy as np
import argparse
import math
import configparser
from pathlib import Path
from pprint import pprint #Nur für Debug benötigt

#Variablen
config_test = True
kreis_durchmesser_mm = 7
min_threshold = 0
max_threshold = 100
oben_links = (400,150)
unten_rechts = (900,600)
fenster_name = "OpenCV"
gauss_faktor = 0
gauss_matrix = (7,7)
clear = lambda: os.system('clear')

# ----------- Config einlesen und überprüfen --------------------------
config = configparser.ConfigParser()
test = Path('config.ini')
if test.is_file():
    print('Config Datei gefunden')
    config.read('config.ini')

else:
    print('Config konnte nicht gefunden werden. Bitte erst mit configGenerator.py eine Config generieren lassen!')
    config_test = False

kreis_durchmesser_pixel = float(config['KREISERKENNUNG']['durchmesserkreisinpixel']) #fragt Wert aus Config File ab

if kreis_durchmesser_pixel == 0:
    kreis_durchmesser_pixel = 1
    print("kreis_durchmesser_pixel war 0 und wurde auf 1 gesetzt")

umrechnung_pixel_mm = kreis_durchmesser_mm / kreis_durchmesser_pixel #Rechnet mm pro Pixel aus

# ----------------------------------- Main Code -----------------------
if config_test:
    cam = cv2.VideoCapture(0);
    while cam.isOpened():
        ret, frame = cam.read()
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
        cv2.circle(ausschnitt,mittelpunkt,2,(0,0,255),3)
        circles = cv2.HoughCircles(ausschnitt,cv2.HOUGH_GRADIENT,1,20,param1=100,param2=20,minRadius=27,maxRadius= 32)
        clear()
        if circles is not None:
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
                    print('X: ' + str(i[0]))
                    print('Y: ' + str(i[1]))
                    print('Radius: ' + str(i[2]))

        print('Mittelpunkt Bild: ' + str(mittelpunkt))
        print('Distanz zum nächsten Kreismittelpunkt (Pixeln): ' + str(kdistanz))
        print('Nächster Kreis: ' + str(kkreis_xy))
        print('geschätzte Distanz (in CM): ' + str((kdistanz*umrechnung_pixel_mm)/10)) # Distanz in Pixeln mal mm Pro Pixel durch 10 für CM

        ausschnitt = cv2.cvtColor(ausschnitt, cv2.COLOR_GRAY2RGB)
        cv2.circle(frame, mittelpunkt, 2, (255,255,255),2) #Mittelpunkt des Bildes
        cv2.circle(frame, kkreis_xy, kkreis_r,(0,255,0),2) #ausgewählter Kreisen
        cv2.circle(frame, kkreis_xy, 2,(0,255,0),2) #Mittelpunkt des Kreises

        if circles is not None: #Damit nur eine Linie gezeichnet wird, wenn er Kreise findet
            cv2.line(frame,mittelpunkt,kkreis_xy,(255,255,255),5) #Linie zwischen Mittelpunkt und ausgewähltem Kreis
            cv2.putText(frame, str(round(kdistanz, 2)) , kkreis_xy, cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA, 0)
            cv2.putText(frame, 'geschaetzte Distanz (in CM): ' + str(round((kdistanz*umrechnung_pixel_mm)/10,2)), (100,100), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA, 0)

        cv2.namedWindow(fenster_name, 1)
        cv2.imshow(fenster_name, frame)
        key = cv2.waitKey(1)
        # Wenn ESC gedrückt wird, wird  das Programm beendet
        if key == 27:
            break
    # Alles beenden
    cam.release()
    cv2.destroyAllWindows()
