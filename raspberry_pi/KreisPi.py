#!/usr/bin/python3
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

cam = PiCamera()
cam.resolution = (640, 480)
cam.framerate = 30
rawCapture = PiRGBArray(cam, size=(640, 480))

time.sleep(1) #eine Sekunde warten, damit die Kamera fokussieren kann detectMultiScale

fenster_name = "Kreiserkennung"

#Variablen die per Trackbar geändert werden sollen
min_threshold = 0
max_threshold = 100

# ----------------------------------- Main Code -----------------------
for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array
    # in Graubild umwandeln
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # mit Gauss blurren
    gauss = cv2.GaussianBlur(frame, (3,3), 1.5)

    blur = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,1,20,param1=100,param2=40,minRadius=1,maxRadius= 150)

    if circles is not None:
        for i in circles[0, :]:
            #Kreis zeichnen
            cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2) #(Quelle, (x,y), Radius, Farbe, )
            #Mittelpunkt maxlen
            cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)

    # Bild anziegen
    cv2.namedWindow(fenster_name, 1)
    #cv2.imshow(fenster_name, canny)
    cv2.imshow(fenster_name, frame)
    #cv2.imshow("Grau", gauss)

    rawCapture.truncate(0)

    #print(canny.dtype)
    key = cv2.waitKey(1)
    # Wenn ESC gedrückt wird, wird  das Programm beendet
    if key == 27:
        break

# Alles beenden
cam.release()
cv2.destroyAllWindows()
