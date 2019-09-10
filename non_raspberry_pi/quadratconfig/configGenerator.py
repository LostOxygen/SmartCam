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
from csv import *
import operator

#Variablen
fenster_name = "OpenCV Quadraterkennung"
seitenlaenge_quadrat = 70 #mm
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

# ----------------------------------- Main Code -----------------------
def sorting(elem):
    return elem[1]

def main():
    cam = cv2.VideoCapture(0);
    while cam.isOpened():
        ret, img = cam.read()

        if img is None:
            print("Fehler bei Laden des frames!" + "!\n")
            return -1

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 1)
        blur = cv2.bilateralFilter(blur, 11, 17, 17)
        blur = cv2.Canny(blur, 30, 120)
        #ausschnitt = blur[oben_links[1] : unten_rechts[1], oben_links[0] : unten_rechts[0]]

        contours, hierarchy = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            #print(box)
            #cv2.drawContours(img, [box], 0, (0,0,255), 2)

            #approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
            gray = np.float32(gray)
            #corners = cv2.cornerHarris(gray, 2, 7, 0.04)
            corners = cv2.goodFeaturesToTrack(gray, 20, 0.11, 100)
            corners = np.int0(corners)
            #corners = cv2.dilate(corners, None)

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

            dist.sort(key=sorting) #sortieren

            #von A zu den beiden nächsten Punkten zeichnen
            cv2.line(img, punktedict["a"], dist[0][0], (255,255,0), 2)
            cv2.line(img, punktedict["a"], dist[1][0], (255,255,0), 2)
            #vom letzten Punkt zu den beiden die nicht A sind zeichnen
            cv2.line(img, dist[2][0], dist[0][0], (255,255,0), 2)
            cv2.line(img, dist[2][0], dist[1][0], (255,255,0), 2)

            print(dist[0])

        cv2.namedWindow(fenster_name, 1)
        cv2.imshow(fenster_name, img)
        key = cv2.waitKey(1)
        # Wenn ESC gedrückt wird, wird  das Programm beendet
        if key == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
