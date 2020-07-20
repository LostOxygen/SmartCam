#!/usr/bin/python3
# -*- coding: utf8 -*-

import logging
import cv2
import sys
import os
import numpy as np
import argparse
import math
from ...core.configLoader import configReader
from pathlib import Path
from pprint import pprint #Nur für Debug benötigt
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from PIL import Image
import io
from datetime import datetime

class circleDetection():
'''
This class takes a picture with the RPI Camera and detects all circles in a specified area and calculates the offset of the nearest circle relatively to the image center
'''

    def __init__(cls):
        pass

    @classmethod
    def detectCircles(cls, picture=False): #Picture is a boolean. True saves the image, false does not

        image_frame = None
        offset = (0,0)
        config_test = True
        kreis_durchmesser_mm = 7
        min_threshold = 0
        max_threshold = 100
        oben_links = (460,144)
        unten_rechts = (1360,1044)
        fenster_name = "Circle Detection"
        gauss_faktor = 0
        gauss_matrix = (7,7)
        clear = lambda: os.system('clear')

        d = datetime.now()
        imgYear = "%04d" % (d.year)
        imgMonth = "%02d" % (d.month)
        imgDate = "%02d" % (d.day)
        imgHour = "%02d" % (d.hour)
        imgMins = "%02d" % (d.minute)
        fileName = "" +str(imgYear) + str(imgMonth) + str(imgDate) + str(imgHour) + str(imgMins) + ".jpg"

        # ----------- read config --------------------------
        try:
            umrechnung_pixel_mm = float(configReader.returnEntry('conversion', 'mm_per_pixel')) #fragt Wert aus Config File ab
        except Exception as e:
            logging.error("could not load config entry " + str(e))
            umrechnung_pixel_mm = 1

        if umrechnung_pixel_mm == 0:
            umrechnung_pixel_mm = 1
            logging.info("set circle diameter to 1 instead of 0!")

        upperLeft = (460, 144)
        upperRight = (1360, 144)
        lowerLeft = (460, 1044)
        lowerRight = (1360, 1044)

        middle = (upperLeft[0] + 0.5*(upperRight[0]-upperLeft[0]), upperLeft[1] + 0.5*(lowerRight[1]-upperLeft[1]))

        oben_links = (int(middle[0] - 450) , int(middle[1] - 450))
        unten_rechts = (int(middle[0] + 450) , int(middle[1] + 450))

        # ----------------------------------- Main Code -----------------------
        # main part which checks first initializes the PiCamera and takes a picture and then looks for circles and their offset
        camera = PiCamera()
        camera.resolution = (1920, 1088)
        camera.hflip = True
        camera.vflip = True

        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        frame = rawCapture.array
        camera.close()
        del camera
        del rawCapture

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)
        rechteck = cv2.rectangle(frame, oben_links, unten_rechts, (100,50,200), 5)

        cv2.putText(frame, str(oben_links) , oben_links, cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_AA, 0)
        cv2.putText(frame, str(unten_rechts) , unten_rechts, cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_AA, 0)
        cv2.putText(frame, str((oben_links[0], unten_rechts[1])) , (oben_links[0], unten_rechts[1]), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_AA, 0)
        cv2.putText(frame, str((unten_rechts[0], oben_links[1])) , (unten_rechts[0], oben_links[1]), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_AA, 0)

        # temp variables
        kdistanz = 100000
        kkreis_r = 0
        kkreis_xy = (0,0)

        # crops the image to it's relevant areas
        ausschnitt = blur[oben_links[1] : unten_rechts[1], oben_links[0] : unten_rechts[0]]
        mittelpunkt = (int(oben_links[0]+(unten_rechts[0]-oben_links[0])/2), int(oben_links[1]+(unten_rechts[1]-oben_links[1])/2))

        cv2.circle(ausschnitt,mittelpunkt,2,(0,0,255),3)
        circles = cv2.HoughCircles(ausschnitt,cv2.HOUGH_GRADIENT,1,20,param1=100,param2=20,minRadius=15,maxRadius= 30)
        if circles is not None:
            logging.info("found circles!")
            for i in circles[0,:]:
                cv2.circle(frame,(int(oben_links[0] + i[0]), int(oben_links[1] + i[1])),i[2],(0,0,255),2) #(Quelle, (x,y) = Center, Radius, Farbe, )
                cv2.circle(frame,(int(oben_links[0] + i[0]), int(oben_links[1] + i[1])),2,(0,0,255),3)

                distanz = math.sqrt(((mittelpunkt[0] - (oben_links[0]+i[0]))**2) + ((mittelpunkt[1] - (oben_links[1]+i[1]))**2))

                if distanz < kdistanz:
                    kdistanz = distanz
                    kkreis_r = i[2]
                    kkreis_xy = (int(oben_links[0] + i[0]), int(oben_links[1] + i[1]))

        ausschnitt = cv2.cvtColor(ausschnitt, cv2.COLOR_GRAY2RGB)
        cv2.circle(frame, mittelpunkt, 2, (255,255,255),2)
        cv2.circle(frame, kkreis_xy, kkreis_r,(0,255,0),2)
        cv2.circle(frame, kkreis_xy, 2,(0,255,0),2)

        # creates a timestamp
        d = datetime.now()
        imgYear = "%04d" % (d.year)
        imgMonth = "%02d" % (d.month)
        imgDate = "%02d" % (d.day)
        imgHour = "%02d" % (d.hour)
        imgMins = "%02d" % (d.minute)
        timestamp = "" + str(imgDate) + "." + str(imgMonth) + "." + str(imgYear) + " " + str(imgHour) + ":" + str(imgMins)

        if circles is not None:
            offset = (mittelpunkt[0] - kkreis_xy[0] , mittelpunkt[1] - kkreis_xy[1])
            offset = (round((offset[0]*umrechnung_pixel_mm),2), round((offset[1]*umrechnung_pixel_mm),2))
            cv2.line(frame,mittelpunkt,kkreis_xy,(255,255,255),5)
            cv2.putText(frame, timestamp + " | " + str(offset[0]) + " mm " + " | " + str(offset[1]) + " mm " + " | " + str(round((kdistanz*umrechnung_pixel_mm),2)) + " mm ", (20,1060), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 2, cv2.LINE_AA, 0)

        else:
            offset = (999999,999999)

        image_frame = frame

        if picture:
            if image_frame is not None:
                path = configReader.returnEntry("options", "imagepath")
                if not os.path.exists(path):
                    try:
                        os.mkdir(path)
                    except Exception as e:
                        logging.error("Image directory couldn't get created.. \n" + str(e))
                cv2.imwrite(path + fileName, image_frame)
                logging.debug("saved image: " + fileName + " in: " + path)
                return True
        else:
            if not os.path.exists(path):
                try:
                    os.mkdir(path)
                except Exception as e:
                    logging.error("Image directory couldn't get created.. \n" + str(e))
            cv2.imwrite(path, frame)
            return offset
