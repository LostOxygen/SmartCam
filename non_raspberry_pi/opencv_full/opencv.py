#!/usr/bin/python3

##########################
# Author: Jonathan Evertz
# Date: 11.2.2019
# Version: 1.0
##########################

import cv2
import sys
import os
import numpy as np
import argparse
import math
from pprint import pprint

#Variablen
min_threshold = 0
max_threshold = 100
oben_links = (400,150)
unten_rechts = (900,600)
fenster_name = "OpenCV"
gauss_faktor = 0
gauss_matrix = (7,7)
clear = lambda: os.system('clear')

#Pfad zum Kaskadenclassifier im OpenCV Verzeichnis
faceCascade = cv2.CascadeClassifier("/opt/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
eyesCascade = cv2.CascadeClassifier("/opt/opencv/data/haarcascades/haarcascade_eye.xml")

#Background soll herausgefiltert werden
backgroundSubstractor = cv2.createBackgroundSubtractorMOG2( 150, 30, False)

argument = argparse.ArgumentParser()
argument.add_argument("--image", required = False, help = "Nicht-Live Version", action ="store_true")
argument.add_argument("--circle", required = False, help = "Kreiserkennung", action ="store_true")
argument.add_argument("--face", required = False, help = "Gesichtserkennung", action ="store_true")
argument.add_argument("--border", required = False, help = "Kantenerkennung", action ="store_true")
argument.add_argument("--selcircles", required = False, help = "Area of Interest mit Kreisen", action ="store_true")
argument.add_argument("--select", required = False, help = "Erstellt eine Area of Interest (nur Live!)", action ="store_true")
args = argument.parse_args()

def gesicht(frame, gray): #Funktion für Gesichtserkennung
    # FaceCascade auf das Bild anwenden
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        )
    # EyeopencvCascade auf das Bild anwenden
    smile = eyesCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30)
        )

    for (x, y, w, h) in faces:
        #Malt ein Rechteckt um das gesicht
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #und setzt einen Text darüber
        cv2.putText(frame,'Gesicht' ,(x, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 240,0), 2, cv2.LINE_AA, 0)

    for (x, y, w, h) in smile:
        #Malt ein Rechteckt um das gesicht
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 100), 1)
        #und setzt einen Text darüber
        cv2.putText(frame,'Augen' ,(x, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0,100), 1, cv2.LINE_AA, 0)

    cv2.namedWindow(fenster_name, 1)
    cv2.imshow(fenster_name, frame)

def kanten(gauss): #Funktion für Kantenerkennung
    canny = cv2.Canny(gauss, min_threshold, max_threshold)
    _, inverted = cv2.threshold(canny, 30, 255, cv2.THRESH_BINARY_INV)
    cv2.namedWindow(fenster_name, 1)
    cv2.imshow(fenster_name, inverted)

def kreis(frame, blur): #Funktion für Kreiserkennung
    #Unterscheidet zwischen Live und nicht live Version
    if args.image:
        circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,1,20,param1=100,param2=40,minRadius=1,maxRadius= 150)
    else:
        circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,1,20,param1=100,param2=50,minRadius=1,maxRadius= 150)

    if circles is not None:
        for i in circles[0, :]:
            #Kreis zeichnen
            cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2) #(Quelle, (x,y) = Center, Radius, Farbe, )
            #Mittelpunkt maxlen
            cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)

    cv2.namedWindow(fenster_name, 1)
    cv2.imshow(fenster_name, frame)

def select(frame, gauss):
    #zeichnet Rechteckt
    rechteck = cv2.rectangle(frame, oben_links, unten_rechts, (100,50,200), 5)
    #verarbeitet den Teil im Rechteck
    canny = cv2.Canny(gauss, min_threshold, max_threshold)
    _, inverted = cv2.threshold(canny, 30, 255, cv2.THRESH_BINARY_INV)
    ausschnitt = inverted[oben_links[1] : unten_rechts[1], oben_links[0] : unten_rechts[0]]
    ausschnitt = cv2.cvtColor(ausschnitt, cv2.COLOR_GRAY2RGB)
    frame[oben_links[1] : unten_rechts[1], oben_links[0] : unten_rechts[0]] = ausschnitt

    cv2.namedWindow(fenster_name, 1)
    cv2.imshow(fenster_name, frame)

def selectcircles(frame, blur):
	#zeichnet Rechteckt
	rechteck = cv2.rectangle(frame, oben_links, unten_rechts, (100,50,200), 5)
	#verarbeitet den Teil im Rechteck
	kdistanz = 1000
	ausschnitt = blur[oben_links[1] : unten_rechts[1], oben_links[0] : unten_rechts[0]]
	#mittelpunkt = (int(oben_links[0] + (unten_rechts[0]-oben_links[0])/2), int(oben_links[1] + (unten_rechts[1]-oben_links[1])/2))
	mittelpunkt = (250, 225)
	cv2.circle(ausschnitt,mittelpunkt,2,(0,0,255),3)
	circles = cv2.HoughCircles(ausschnitt,cv2.HOUGH_GRADIENT,1,20,param1=100,param2=20,minRadius=27,maxRadius= 32)
	if circles is not None:
		for i in circles[0, :]:
			#Kreis zeichnen
			cv2.circle(ausschnitt,(i[0],i[1]),i[2],(0,255,0),2) #(Quelle, (x,y) = Center, Radius, Farbe, )
			#Mittelpunkt maxlen
			cv2.circle(ausschnitt,(i[0],i[1]),2,(0,0,255),3)
			distanz = ((((i[0]-mittelpunkt[0])**2)+((i[1]-mittelpunkt[1])**2)))
			if math.sqrt(distanz) < kdistanz:
				kdistanz = math.sqrt(distanz)
				kkreis_r = i[2]
				kkreis_xy = (i[0],i[1])
	#clear()
	#print("X: ")
	#print(str(i[0]))
	#print("Y: ")
	#print(str(i[1]))
	#print("Radius: ")
	#print(i[2])
	print("Mittelpunkt Bild: ")
	print(str(mittelpunkt))
	print("Distanz zum nächsten Kreismittelpunkt: ")
	print(str(math.sqrt(kdistanz)))
	print(str(kkreis_xy))
	cv2.circle(ausschnitt, mittelpunkt, 2, (255,255,255),2)
	cv2.circle(ausschnitt, kkreis_xy, kkreis_r,(255,255,255),2)
	print("Nächster Kreis: ")
	print(str(kkreis_xy))
	#frame[oben_links[1] : unten_rechts[1], oben_links[0] : unten_rechts[0]] = ausschnitt
	cv2.namedWindow(fenster_name, 1)
	cv2.imshow(fenster_name, ausschnitt)

def main():
    if args.image:
        filename = input('Dateiname eingeben: ')
        frame = cv2.imread(filename, cv2.IMREAD_COLOR)

        if frame is None:
            print ('Fehler beim Laden des Bildes: ' + filename + '! \n')
            return -1

        # in Graubild umwandeln
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # mit Gauss blurren
        gauss = cv2.GaussianBlur(gray, gauss_matrix, gauss_faktor)
        #weichzeichner für Kreiserkennung
        blur = cv2.medianBlur(gray, 5)

        if args.circle: #Wenn Parameter --circle
            kreis(frame, blur)

        if args.face: #Wenn Parameter --face
            gesicht(frame, gray)

        if args.border: #Wenn Parameter --border
            kanten(gauss)

        cv2.waitKey(0)
    else:
        cam = cv2.VideoCapture(0)
        while cam.isOpened():

            ret, frame = cam.read()
            # in Graubild umwandeln
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # mit Gauss blurren
            gauss = cv2.GaussianBlur(gray, gauss_matrix, gauss_faktor)
            #weichzeichner für Kreiserkennung
            blur = cv2.medianBlur(gray, 5)

            if args.circle: #Wenn Parameter --circle
                kreis(frame, blur)

            if args.face: #Wenn Parameter --face
                gesicht(frame, gray)

            if args.border: #Wenn Parameter --border
                kanten(gauss)

            if args.select: #Wenn Parameter --select
                select(frame, gauss)

            if args.selcircles: #Wenn Parameter --selcircles
                selectcircles(frame, blur)

            key = cv2.waitKey(1)
            # Wenn ESC gedrückt wird, wird  das Programm beendet
            if key == 27:
                break
        # Alles beenden
        cam.release()
        cv2.destroyAllWindows()
    return 0

if __name__ == '__main__':
    main()
