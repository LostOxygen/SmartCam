#!/usr/bin/python3
import cv2
import sys
import numpy as np
from pprint import pprint

fenster_name = "Kreiserkennung"

# ----------------------------------- Main Code -----------------------
def main(argv):
    filename = argv[0]
    frame = cv2.imread(filename, cv2.IMREAD_COLOR)

    if frame is None:
        print ('Fehler beim Laden des Bildes: ' + filename + '! \n')
        return -1

    # in Graubild umwandeln
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # mit Gauss blurren
    gauss = cv2.GaussianBlur(frame, (3,3), 1.5)

    blur = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,1,20,param1=100,param2=40,minRadius=1,maxRadius= 150)

    if circles is not None:
        for i in circles[0, :]:
            #Kreis zeichnen
            cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2) #(Quelle, (x,y) = Center, Radius, Farbe, )
            #Mittelpunkt maxlen
            cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)

    # Bild anziegen
    cv2.namedWindow(fenster_name, 1)
    #cv2.imshow(fenster_name, canny)
    cv2.imshow(fenster_name, frame)
    #cv2.imshow("Grau", gauss)

    cv2.waitKey(0)


if __name__ == "__main__":
    main(sys.argv[1:])
