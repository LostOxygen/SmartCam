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

class Config():
    def createConfig(camera):
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
        frame = camera.get_frame_cv()
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
                kkreis_r = i[2]
                kkreis_xy = (int(oben_links[0] + i[0]), int(oben_links[1] + i[1]))
        else:
            print("kein Kreis für Configerstellung gefunden")
            return False

        config['CONFIG'] = {'post' : '192.168.8.xxx' , 'port' : '65432' , 'AbstandZumObjekt' : '15', 'DurchmesserKreisInPixel' : kkreis_r}
        with open('../config.ini', 'w') as configfile: #Werte in Config schreiben
            config.write(configfile)
        print("Durchmesser Kreis in Pixel: " + str(kkreis_r))
        return True








#area = cv2.contourArea(cnt)
#rect = cv2.minAreaRect(cnt)
#box = cv2.boxPoints(rect)
#box = np.int0(box)

#gray = np.float32(gray)
#corners = cv2.goodFeaturesToTrack(gray, 20, 0.11, 100)
#corners = np.int0(corners)

#------------------- Quadrat aufspannen ----------------------
#dist = [] #zum sortieren der Distanzen
#ecken = [] #die entgültigen Ecken
#punktedict = {
#    "a" : (0,0),
#    "b" : (0,0),
#    "c" : (0,0),
#    "d" : (0,0)
#}

#punkte = []
#for corner in corners:
#    x,y = corner.ravel()
#    punkte.append((x,y))
#    cv2.circle(img, (x, y), 2, (255,255,0), 2)

#punktedict["a"] = punkte[0] #erster Punkt ist Punkt a
#punktedict["b"] = punkte[1] #erster Punkt ist Punkt a
#punktedict["c"] = punkte[2] #erster Punkt ist Punkt a
#punktedict["d"] = punkte[3] #erster Punkt ist Punkt a

#dist_ab = math.sqrt((punkte[0][0] -  punkte[1][0])**2 + (punkte[0][1] - punkte[1][1])**2)
#dist_ac = math.sqrt((punkte[0][0] -  punkte[2][0])**2 + (punkte[0][1] - punkte[2][1])**2)
#dist_ad = math.sqrt((punkte[0][0] -  punkte[3][0])**2 + (punkte[0][1] - punkte[3][1])**2)

#dist.append(((punkte[1][0], punkte[1][1]), dist_ab))
#dist.append(((punkte[2][0], punkte[2][1]), dist_ac))
#dist.append(((punkte[3][0], punkte[3][1]), dist_ad))

#dist.sort(key=lambda elem: elem[1]) #sortieren
#von A zu den beiden nächsten Punkten zeichnen
#cv2.line(img, punktedict["a"], dist[0][0], (255,255,0), 2)
#cv2.line(img, punktedict["a"], dist[1][0], (255,255,0), 2)
#vom letzten Punkt zu den beiden die nicht A sind zeichnen
#cv2.line(img, dist[2][0], dist[0][0], (255,255,0), 2)
#cv2.line(img, dist[2][0], dist[1][0], (255,255,0), 2)

#try:
    #conversion erstellen
#    edge_x1 = dist[0][1]
#    edge_x2 = dist[1][1]
#    edge_y1 = dist[0][1]
#    edge_y2 = dist[1][1]

#    edge_x1_mm = (edgelength / edge_x1) #conversion in mm per pixel
#    edge_x2_mm = (edgelength / edge_x2)
#    edge_y1_mm = (edgelength / edge_y1)
#    edge_y2_mm = (edgelength / edge_y2)

#    mean = (edge_x1_mm + edge_x2_mm + edge_y1_mm + edge_y2_mm) / 4
#    conversion_mm_per_pixel = mean

#    edges = (edge_x1, edge_x2, edge_y1, edge_y2)

#except:
#    print("Fehler: womöglich wurden keine Kanten gefunden .. ")
#    conversion_mm_per_pixel = 1
#    edges = (1, 1, 1, 1)
