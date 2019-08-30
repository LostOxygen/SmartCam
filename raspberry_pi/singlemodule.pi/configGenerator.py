#!/usr/bin/python3

##########################
# Author: Jonathan Evertz
# Date: 07.03.2019
# Generator für OpenCV Config File
##########################

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

cam = PiCamera()
cam.resolution = (1920, 1088)
cam.framerate = 30
rawCapture = PiRGBArray(cam, size=(1920, 1088))

time.sleep(1) #eine Sekunde warten, damit die Kamera fokussieren kann

#Variablen
kreis_durchmesser_mm = 7
min_threshold = 0
max_threshold = 100
oben_links = (400,150)
unten_rechts = (900,600)
fenster_name = "OpenCV"
gauss_faktor = 0
gauss_matrix = (7,7)
clear = lambda: os.system('clear')
config = configparser.ConfigParser()

# ----------------------------------- Main Code -----------------------
cam = cv2.VideoCapture(0);
while cam.isOpened():
    ret, frame = cam.read()
    # in Graubild umwandeln
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #blurren
    blur = cv2.medianBlur(gray, 5)
    #zeichnet Rechteckt
    rechteck = cv2.rectangle(frame, oben_links, unten_rechts, (100,50,200), 5)
    #Temp Variablen zum arbeiten für nächsten Kreis
    kdistanz = 100000
    kkreis_r = 0
    kkreis_xy = (0,0)
    #verarbeitet den Teil im Rechteck
    ausschnitt = blur[oben_links[1] : unten_rechts[1], oben_links[0] : unten_rechts[0]]
    mittelpunkt = (int(oben_links[0]+(unten_rechts[0]-oben_links[0])/2), int(oben_links[1]+(unten_rechts[1]-oben_links[1])/2))
    cv2.circle(ausschnitt,mittelpunkt,2,(0,0,255),3)
    circles = cv2.HoughCircles(ausschnitt,cv2.HOUGH_GRADIENT,1,20,param1=100,param2=20,minRadius=27,maxRadius= 32)
    if circles is not None:
        for i in circles[0,:]:
			#Kreis zeichnen
            cv2.circle(ausschnitt,(i[0],i[1]),i[2],(0,255,0),2) #(Quelle, (x,y) = Center, Radius, Farbe, )
            #Mittelpunkt malen
            cv2.circle(ausschnitt,(i[0],i[1]),2,(0,0,255),3)
            #den nächsten Kreis finden
            kkreis_r = i[2]
            kkreis_xy = (int(oben_links[0] + i[0]), int(oben_links[1] + i[1]))

    ausschnitt = cv2.cvtColor(ausschnitt, cv2.COLOR_GRAY2RGB)
    cv2.circle(frame, mittelpunkt, 2, (255,255,255),2) #Mittelpunkt des Bildes
    cv2.circle(frame, kkreis_xy, kkreis_r,(0,255,0),2) #ausgewählter Kreisen
    cv2.circle(frame, kkreis_xy, 2,(0,255,0),2) #Mittelpunkt des Kreises

    cv2.namedWindow(fenster_name, 1)
    cv2.imshow(fenster_name, frame)

    config['CONFIG'] = {'AbstandZumObjekt' : '15', 'DurchmesserKreisInPixel' : kkreis_r}
    with open('config.ini', 'w') as configfile: #Werte in Config schreiben
        config.write(configfile)

    key = cv2.waitKey(1)
    # Wenn ESC gedrückt wird, wird  das Programm beendet
    if key == 27:
        break
    # Alles beenden
cam.release()
cv2.destroyAllWindows()
