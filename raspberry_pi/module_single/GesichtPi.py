#!/usr/bin/python3
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import numpy as np

#Pfad zum Kaskadenclassifier im OpenCV Verzeichnis
faceCascade = cv2.CascadeClassifier("/opt/opencv/data/haarcascades/haarcascade_frontalface_default.xml")

cam = PiCamera()
cam.resolution = (640, 480)
cam.framerate = 30
rawCapture = PiRGBArray(cam, size=(640, 480))

time.sleep(1) #eine Sekunde warten, damit die Kamera fokussieren kann

for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array
    # in Graubild umwandeln
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # FaceCascade auf das Bild anwenden
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        )

    for (x, y, w, h) in faces:
        #Malt ein Rechteckt um das gesicht
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #und setzt einen Text darüber
        cv2.putText(frame,'Gesicht' ,(x, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 240,0), 2, cv2.LINE_AA, 0)

    cv2.imshow("Gesicht", frame)

    key = cv2.waitKey(1)
    # Wenn ESC gedrückt wird, wird  das Programm beendet
    if key == 27:
        break

cv2.destroyAllWindows()
