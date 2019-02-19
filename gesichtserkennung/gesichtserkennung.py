#!/usr/bin/python3
import cv2
import sys
import numpy as np
from pprint import pprint

fenster_name = "Kantenerkennung"

#Variablen die per Trackbar geändert werden sollen
min_threshold = 0
max_threshold = 100

#Pfad zum Kaskadenclassifier im OpenCV Verzeichnis
faceCascade = cv2.CascadeClassifier("/opt/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
eyesCascade = cv2.CascadeClassifier("/opt/opencv/data/haarcascades/haarcascade_eye.xml")

#Background soll herausgefiltert werden
backgroundSubstractor = cv2.createBackgroundSubtractorMOG2( 150, 30, False)

#----------------------------- Trackbar -------------------------------
def trackbar(val):
    pprint(val)
    min_threshold = val
# ----------------------------------- Main Code -----------------------
cam = cv2.VideoCapture(0);
while cam.isOpened():
    ret, frame = cam.read()

    #Trackbar zum einstellen des Thresholds
    trackbar_name = 'Threshold: %d' % min_threshold
    cv2.createTrackbar("Threshold: ", fenster_name, 0, 100, trackbar)

    # in Graubild umwandeln
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # FaceCascade auf das Bild anwenden
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        )
    # Eyeopencv sCascade auf das Bild anwenden
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

    #fgmask = backgroundSubstractor.apply(frame)

    # mit Gauss blurren
    gauss = cv2.GaussianBlur(gray, (3,3), 1.5)
    # Canny um Kanten dann zu erkennen
    canny = cv2.Canny(gauss, min_threshold, max_threshold)

    trackbar(0)
    # Bild anziegen
    cv2.namedWindow(fenster_name, 1)
    cv2.imshow(fenster_name, canny)
    cv2.imshow("Gesichtserkennung", frame)
    #cv2.imshow("Grau", gauss)

    #print(canny.dtype)
    key = cv2.waitKey(1)
    # Wenn ESC gedrückt wird, wird  das Programm beendet
    if key == 27:
        break

# Alles beenden
cam.release()
cv2.destroyAllWindows()
