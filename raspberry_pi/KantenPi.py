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

for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array
    # in Graubild umwandeln
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # mit Gauss blurren
    gauss = cv2.GaussianBlur(gray, (3,3), 1.5)
    # Canny um Kanten dann zu erkennen
    canny = cv2.Canny(gauss, 0, 100)
    # Bild anziegen
    cv2.imshow("Kanten", canny)

    rawCapture.truncate(0)

    key = cv2.waitKey(1)
    # Wenn ESC gedrückt wird, wird  das Programm beendet
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()
