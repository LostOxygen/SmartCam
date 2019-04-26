#!/usr/bin/env python3
# -*- coding: utf8 -*-

import cv2
import sys
import os
import numpy as np
import argparse
import math
import configparser
from pathlib import Path
from pprint import pprint #Nur für Debug benötigt
from matplotlib import pyplot as plt

#Variablen
fenster_name = "Kabelerkenung"
mittelpunkt = (int(1920/2), int(1080/2))

def main(argv):
    filename = argv[0]
    img = cv2.imread(filename, cv2.IMREAD_COLOR)

    if img is None:
        print("Fehler bei Laden der Datei: " + filename + "!\n")
        return -1

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 300, 0.01, 10)
    corners = np.int0(corners)

    min_xy = (1000,1000) #temp Var zum finden von punkt ganz oben_links
    for i in corners:
        x,y = i.ravel()
        cv2.circle(img, (x,y), 2, (0,0,255), 2)
        if x < min_xy[0]: #guckt nach kleinstem x wert
            min_xy = (x,y)
            print(min_xy)

    cv2.circle(img, min_xy, 2, (0,255,0), 2) #zeichnet punkt ganz links
    cv2.line(img, min_xy, (min_xy[0], mittelpunkt[1]), (255,255,0), 2) #zeichnet linie von punkt nach oben
    #zeichnet Mittelpunkt und Linie nach links
    cv2.circle(img, mittelpunkt, 2, (255,255,0), 2)
    cv2.line(img, mittelpunkt, (min_xy[0],mittelpunkt[1]), (255,255,0), 2)
    cv2.line(img, mittelpunkt, min_xy, (255,255,0), 2)

    cv2.namedWindow(fenster_name, 1)
    cv2.imshow(fenster_name, img)
    cv2.waitKey(0)

    #plt.imshow(img), plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
