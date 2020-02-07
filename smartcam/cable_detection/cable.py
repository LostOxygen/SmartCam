#!/usr/bin/env python3
# -*- coding: utf8 -*-

import logging

import cv2
import sys
import os
import numpy as np
import argparse
import math
import imutils
from ..configLoader import configReader
from pathlib import Path
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from PIL import Image
import io
from datetime import datetime

class cableDetection():
    def __init__(cls):
        pass


    #Variablen
    fenster_name = "Cable Detection"
    detection_size = (500, 500)
    config_test = True
    umrechnung_pixel_mm = 1 #to avoid errors the value is preset to 1
    maxCorners = 300 #Anzahl zu erkennenden Kanten
    qualityLevel = 0.03 #je höher desto genauer
    minDistance = 10 #mindeste Distanz zwischen Punkten

    @classmethod
    def visualization_rgb(cls, img, min_xy, height, mittelpunkt, dist_x_mm, dist_y_mm, dist_x, dist_y):
    #visualization of the rgb picture
        cv2.circle(img, min_xy, 4, (255, 255, 255), 4) #zeichnet punkt ganz links
        cv2.line(img, min_xy, (min_xy[0], int(height/2)), (255,255,255), 2) #zeichnet linie von punkt nach oben
        #zeichnet Mittelpunkt und Linie nach links
        cv2.circle(img, mittelpunkt, 2, (255,255,255), 2)
        cv2.line(img, mittelpunkt, (min_xy[0], int(height/2)), (255,255,255), 2)
        cv2.line(img, mittelpunkt, min_xy, (255,255,255), 2)
        d = datetime.now()
        imgYear = "%04d" % (d.year)
        imgMonth = "%02d" % (d.month)
        imgDate = "%02d" % (d.day)
        imgHour = "%02d" % (d.hour)
        imgMins = "%02d" % (d.minute)
        timestamp = "" + str(imgDate) + "." + str(imgMonth) + "." + str(imgYear) + " " + str(imgHour) + ":" + str(imgMins)
        cv2.putText(img, timestamp + " | " + str(round(dist_x_mm, 2)) + " mm | " + str(round(dist_y_mm, 2)) + " mm ", (20,1060), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 2, cv2.LINE_AA, 0)

        logging.info("distance_Y: " + str(dist_y))
        logging.info("converted: " + str(round(dist_y_mm, 2)) + "mm")

    @classmethod
    def visualization_gray(cls, gray, extLeft, g_height, g_mittelpunkt):
        cv2.circle(gray, extLeft, 4, (255, 255, 255), 4) #zeichnet punkt ganz links
        cv2.line(gray, extLeft, (extLeft[0], int(g_height/2)), (255,255,255), 2) #zeichnet linie von punkt nach oben
        #zeichnet Mittelpunkt und Linie nach links
        cv2.circle(gray, g_mittelpunkt, 2, (255,255,255), 2)
        cv2.line(gray, g_mittelpunkt, (extLeft[0], int(g_height/2)), (255,255,255), 2)
        cv2.line(gray, g_mittelpunkt, extLeft, (255,255,255), 2)

    @classmethod
    def saveImg(cls, bild_num, img, gray):
        #if str(bild_num) == "1":
        logging.info("saved cable1.jpg and cablegray1.jpg in ../images/")
        cv2.imwrite("../images/cablegray1.jpg", gray)
        cv2.imwrite("../images/cable1.jpg", img)
        # elif str(bild_num) == "2":
        #     logging.info("saved cable2.jpg and cablegray2.jpg in ../images/")
        #     cv2.imwrite("../images/cablegray2.jpg", gray)
        #     cv2.imwrite("../images/cable2.jpg", img) #speichert ein Bild

    @classmethod
    def config(cls):
        cls.umrechnung_pixel_mm = float(configReader.returnEntry('conversion', 'mm_per_pixel1')) #fragt Wert aus Config File ab

    @classmethod
    def rotate(cls, img, mittelpunkt, width, height):
        rotation_mat = cv2.getRotationMatrix2D(mittelpunkt, 180, 1.)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mat[0,0])
        abs_sin = abs(rotation_mat[0,1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origo) and adding the new image center coordinates
        rotation_mat[0, 2] += bound_w/2 - mittelpunkt[0]
        rotation_mat[1, 2] += bound_h/2 - mittelpunkt[1]

        # rotate image with the new bounds and translated rotation matrix
        img = cv2.warpAffine(img, rotation_mat, (bound_w, bound_h))
        return img

    @classmethod
    def detectCable(cls, bild_num=1):
        #main part which checks for wires and their angle
        camera = PiCamera()
        camera.resolution = (1920, 1088)
        camera.hflip = True
        camera.vflip = True
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        img = rawCapture.array
        del camera
        del rawCapture

        height, width = img.shape[:2] # image shape has 3 dimensions
        mittelpunkt = (int(width/2), int(height/2)) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape
        img = cls.rotate(img, mittelpunkt, width, height)  #rotiert das Bild ggf.
        height, width = img.shape[:2]

        oben_links = (int(mittelpunkt[0]- cls.detection_size[0]), int(mittelpunkt[1]- cls.detection_size[1]/2))
        unten_rechts = (int(mittelpunkt[0]), int(mittelpunkt[1]+ cls.detection_size[1]/2))

        if img is None: #to prevent errors with empty images
            logging.error("Could not load frame properly..")
            return -1

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = gray[int(oben_links[1]) : int(unten_rechts[1]), int(oben_links[0]) : int(unten_rechts[0])] #schneidet graubild auf relevanten Bereich zu
        blur = cv2.GaussianBlur(gray, (7,7), 1)
        blur = cv2.bilateralFilter(blur, 11, 17, 17)
        blur = cv2.Canny(blur, 30, 120)

        contours = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Konturen suchen
        #corners = cv2.goodFeaturesToTrack(gray, cls.maxCorners, cls.qualityLevel, cls.minDistance)
        cv2.drawContours(gray, contours[0], -1, (0,255,0), 3)

        contours = imutils.grab_contours(contours)
        try:
            cnts = max(contours, key=cv2.contourArea)
            extLeft = tuple(cnts[cnts[:, :, 0].argmin()][0])
        except Exception as e:
            logging.error(e)
            logging.error("Could not find any contours..")
            extLeft = (0,0)

        g_height, g_width = gray.shape[:2]
        g_mittelpunkt = (g_width, int(g_height/2))
        cls.visualization_gray(gray, extLeft, g_height, g_mittelpunkt)

        min_xy = extLeft #temp Var zum finden von punkt ganz oben_links
        #if corners is not None:
        #    for i in corners:
        #        x,y = i.ravel()
        #        if x <= 1100: #zeichnet nur Relevante Punkte
        #            cv2.circle(gray, (x,y), 2, (255, 255, 255), 2)
        #            cv2.circle(img, (int(mittelpunkt[0] - int(g_mittelpunkt[0] - x)), int(mittelpunkt[1] - int(g_mittelpunkt[1] - y))), 2, (255, 255, 255), 2) #rechnet auf ganzes Bild um und zeichnet Punkte ein
        #        if x < min_xy[0]: #guckt nach kleinstem x wert
        #            min_xy = (x,y)

        dist_y = g_mittelpunkt[1] - min_xy[1]
        dist_x = g_mittelpunkt[0] - min_xy[0]
        min_xy = (int(mittelpunkt[0] - dist_x), int(mittelpunkt[1] - dist_y)) #rechnet min_xy auf das gesamte Bild um
        dist_y_mm = (dist_y * cls.umrechnung_pixel_mm)/2
        dist_x_mm = (dist_x * cls.umrechnung_pixel_mm)/2

        cls.visualization_rgb(img, min_xy, height, mittelpunkt, dist_x_mm, dist_y_mm, dist_x, dist_y)

        cls.saveImg(bild_num, img, gray)
        offset = (round(dist_x_mm, 2), round(dist_y_mm, 2))

        return offset
