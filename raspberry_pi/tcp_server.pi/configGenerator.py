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
import socket
import fcntl
import struct
import csv

# ----------------------------------- Main Code -----------------------
class Config:
    def sorting(elem):
        return elem[1]

    def createConfig(self, camera, img_order, height):
        #Variablen
        edgelength = 70 #in mm und standardwert
        min_threshold = 0
        max_threshold = 100
        kernel = np.ones((5, 5), np.uint8)
        gauss_faktor = 0
        gauss_matrix = (7,7)
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

        try:
            Config.createCSV(contours[0], "contours")
        except IndexError as e:
            print("Nicht genug Konturen für <contours> gefunden.")
            print(e)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            gray = np.float32(gray)
            corners = cv2.goodFeaturesToTrack(gray, 20, 0.11, 100)
            corners = np.int0(corners)

#------------------- Quadrat aufspannen ----------------------
            dist = [] #zum sortieren der Distanzen
            ecken = [] #die entgültigen Ecken
            punktedict = {
                "a" : (0,0),
                "b" : (0,0),
                "c" : (0,0),
                "d" : (0,0)
            }

            punkte = []
            for corner in corners:
                x,y = corner.ravel()
                punkte.append((x,y))
                cv2.circle(img, (x, y), 2, (255,255,0), 2)

            punktedict["a"] = punkte[0] #erster Punkt ist Punkt a
            cv2.putText(img, "A" , punktedict["a"], cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)
            punktedict["b"] = punkte[1] #erster Punkt ist Punkt a
            cv2.putText(img, "B" , punktedict["b"], cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)
            punktedict["c"] = punkte[2] #erster Punkt ist Punkt a
            cv2.putText(img, "C" , punktedict["c"], cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)
            punktedict["d"] = punkte[3] #erster Punkt ist Punkt a
            cv2.putText(img, "D" , punktedict["d"], cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)

            dist_ab = math.sqrt((punkte[0][0] -  punkte[1][0])**2 + (punkte[0][1] - punkte[1][1])**2)
            dist_ac = math.sqrt((punkte[0][0] -  punkte[2][0])**2 + (punkte[0][1] - punkte[2][1])**2)
            dist_ad = math.sqrt((punkte[0][0] -  punkte[3][0])**2 + (punkte[0][1] - punkte[3][1])**2)

            dist.append(((punkte[1][0], punkte[1][1]), dist_ab))
            dist.append(((punkte[2][0], punkte[2][1]), dist_ac))
            dist.append(((punkte[3][0], punkte[3][1]), dist_ad))

            dist.sort(key=self.sorting) #sortieren

            #von A zu den beiden nächsten Punkten zeichnen
            cv2.line(img, punktedict["a"], dist[0][0], (255,255,0), 2)
            cv2.line(img, punktedict["a"], dist[1][0], (255,255,0), 2)
            #vom letzten Punkt zu den beiden die nicht A sind zeichnen
            cv2.line(img, dist[2][0], dist[0][0], (255,255,0), 2)
            cv2.line(img, dist[2][0], dist[1][0], (255,255,0), 2)

            try:
                #conversion erstellen
                edge_x1 = dist[0][1]
                edge_x2 = dist[1][1]
                edge_y1 = dist[0][1]
                edge_y2 = dist[1][1]

                edge_x1_mm = (edgelength / edge_x1) #conversion in mm per pixel
                edge_x2_mm = (edgelength / edge_x2)
                edge_y1_mm = (edgelength / edge_y1)
                edge_y2_mm = (edgelength / edge_y2)

                mean = (edge_x1_mm + edge_x2_mm + edge_y1_mm + edge_y2_mm) / 4
                conversion_mm_per_pixel = mean

                edges = (edge_x1, edge_x2, edge_y1, edge_y2)

            except:
                print("Fehler: womöglich wurden keine Kanten gefunden .. ")
                conversion_mm_per_pixel = 1
                edges = (1, 1, 1, 1)

            Config.writeConfig(img_order, height, conversion_mm_per_pixel, edges) #writes the .ini file

            img = Config.visualization(img, (upperLeft, upperRight, lowerLeft, lowerRight), edges) #writes text and draws the rectangel into the img

        Config.saveImg(img_order, img) #saves img at the end

# ----------------------------------- Config -----------------------
    def writeConfig(img_order, height, conversion_mm_per_pixel, edges):
        configpar = configparser.ConfigParser()

        if str(img_order) == "1":
            configpar['tcp'] = {'host' : '192.168.8.6x',
                             'port' : '65432'}
            configpar['web'] = {'web_host' : '134.147.234.23x',
                             'web_port' : '80'}
            configpar['conversion'] = {'distanceToObject1' : height,
                                    'mm_per_pixel1' : conversion_mm_per_pixel,
                                    'distanceToObject2' : 0,
                                    'scalingFactor' : 1}
            configpar['edges1'] = {'edge_x1' : edges[0],
                               'edge_x2' : edges[1],
                               'edge_y1' : edges[2],
                               'edge_y2' : edges[3]}
            with open('../config.ini', 'w') as configfile: #writes config
                configpar.write(configfile)

        elif str(img_order) == "2":
            if Path('../config.ini').is_file():
                configpar.read('../config.ini')

                temp_dist1 = float(configpar['conversion']['distanceToObject1'])
                mm_per_pixel1 = float(configpar['conversion']['mm_per_pixel1'])

                distanceToObject1 = temp_dist1
                distanceToObject2 = float(height)

                scalingFactor = round((mm_per_pixel1 / conversion_mm_per_pixel) / abs(distanceToObject1 - distanceToObject2), 9)

                configpar.set('conversion', 'distanceToObject2', distanceToObject2) #updating the values
                configpar.set('conversion', 'scalingFactor', scalingFactor)
                configpar.set('conversion', 'mm_per_pixel2', conversion_mm_per_pixel)

                configpar['edges2'] = {'edge_x1' : edges[0],
                                   'edge_x2' : edges[1],
                                   'edge_y1' : edges[2],
                                   'edge_y2' : edges[3]}

                with open('../config.ini', 'wb') as configfile: #Writeback values into config
                    configpar.write(configfile)
            else:
                print("Config Datei nicht gefunden")

# ----------------------------------- Timestamp -----------------------
    def getTimestamp():
        d = datetime.now()
        imgYear = "%04d" % (d.year)
        imgMonth = "%02d" % (d.month)
        imgDate = "%02d" % (d.day)
        imgHour = "%02d" % (d.hour)
        imgMins = "%02d" % (d.minute)
        imgSecs = "%02d" % (d.second)
        timestamp = "" + str(imgDate) + "." + str(imgMonth) + "." + str(imgYear) + " " + str(imgHour) + ":" + str(imgMins) + ":" + str(imgSecs)
        return timestamp

# ----------------------------------- Visual -----------------------
    def visualization(img, points, edges):
        #cv2.drawContours(img, [approx] ,0,(0,0,255),3)
        cv2.circle(img, points[0], 2, (255,255,0), 2) #oben links
        cv2.circle(img, points[1], 2, (255,255,0), 2) #oben rechts
        cv2.circle(img, points[2], 2, (255,255,0), 2) #unten links
        cv2.circle(img, points[3], 2, (255,255,0), 2) #unten rechts

        cv2.putText(img, "edge_x1 = " + str(edges[0]), (100,100), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)
        cv2.putText(img, "edge_y1 = " + str(edges[1]) , (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)
        cv2.putText(img, "edge_x2 = " + str(edges[2]), (100,200), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)
        cv2.putText(img, "edge_y2 = " + str(edges[3]), (100,250), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)

        return img

# ----------------------------------- Save Img -----------------------
    def saveImg(img_order, img):

        timestamp = Config.getTimestamp()
        cv2.putText(img, "time = " + timestamp, (100,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA, 0)

        if str(img_order) == "1":
            #np.savetxt("../bilder/contours1.csv", contours) #speichret konturen als csv
            print("speichert quadrat1.jpg in /home/pi/RoboSchalt/raspberry_pi/bilder/")
            cv2.imwrite("../bilder/quadrat1.jpg", img) #speichert ein Bild
        elif str(img_order) == "2":
            #np.savetxt("../bilder/contours2.csv", contours) #speichret konturen als csv
            print("speichert quadrat2.jpg in /home/pi/RoboSchalt/raspberry_pi/bilder/")
            cv2.imwrite("../bilder/quadrat2.jpg", img)
        else:
            print("Wert: " + str(img_order))

# ----------------------------------- get IP -----------------------
    def get_ip(interface):
        ip_addr = "Not connected"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            ip_addr = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', interface[:15]))[20:24])
        finally:
            return ip_addr

# ----------------------------------- save as CSV -----------------------
    def createCSV(array, name):
        path = "../bilder/" + name + ".csv"
        f = open(path, 'w+')
        wr = csv.writer(f)
        wr.writerows(array)
