#!/usr/bin/env python3
# -*- coding: utf8 -*-
import logging
import cv2
import sys
import numpy as np
from ..configLoader import configReader
from picamera.array import PiRGBArray
from picamera import PiCamera

class Calibration:
    min_threshold = 0
    max_threshold = 100
    kernel = np.ones((5, 5), np.uint8)
    gauss_faktor = 0
    gauss_matrix = (7,7)
    maxCorners = 300 #Anzahl zu erkennenden Kanten
    qualityLevel = 0.03 #je höher desto genauer
    minDistance = 10 #mindeste Distanz zwischen Punkten

    def __init__(cls):
        pass


    @classmethod
    def calibrate(cls):
        try:
            cls.realMeasurement = configReader.returnEntry("calibration", "realMeasurement")
        except Exception as e:
            logging.warning("couldn't get measurement data from config file.. \n" + e.message)

        digitalMeasurement = cls.scan()

        cls.mmPerPixel =  cls.realMeasurement / digitalMeasurement
        logging.info("calibration successful. Calibration Data: " + str(cls.mmPerPixel) + "mm per pixel")

        try:
            configReader.updateConfig("calibration", "mmPerPixel", cls.mmPerPixel)
        except Exception as e:
            logging.warning("couldn't update config properly .. \n" + e.message)

    @classmethod
    def scan(cls):
        camera = PiCamera()
        camera.resolution = (1920, 1080)
        camera.hflip = True
        camera.vflip = True
        digitalMeasurement = 1

        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        img = rawCapture.array

        if img is None:
            logging.warning("Could not load frame!" + "!\n")
            return -1

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7,7), 1)
        blur = cv2.bilateralFilter(blur, 11, 17, 17)
        blur = cv2.Canny(blur, 30, 120)

        image_info = blur.shape

        contours, hierarchy = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            #if area > 0: #an die geforderte Größe anpassen

            approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)

            x_values = [] #Listen für x und y werte um die passenden rauszusuchen
            y_values = []

            for i in approx:
                x_values.append(i[0][0])
                y_values.append(i[0][1])

            upperLeft = (min(x_values), min(y_values))
            upperRight = (max(x_values), min(y_values))
            lowerLeft = (min(x_values), max(y_values))
            lowerRight = (max(x_values), max(y_values))

            MinMaxValues = (min(x_values), min(y_values), max(x_values), max(y_values))
            points = (upperLeft, upperRight, lowerLeft, lowerRight)

            edge_x1 = math.sqrt((upperLeft[0] - upperRight[0])**2 + (upperLeft[1] - upperRight[1])**2)
            edge_x2 = math.sqrt((lowerLeft[0] - lowerRight[0])**2 + (lowerLeft[1] - lowerRight[1])**2)
            edge_y1 = math.sqrt((upperLeft[0] - lowerLeft[0])**2 + (upperLeft[1] - lowerLeft[1])**2)
            edge_y2 = math.sqrt((upperRight[0] - lowerRight[0])**2 + (upperRight[1] - lowerRight[1])**2)

            digitalMeasurement = np.mean([edge_x1, edge_x2, edge_y1, edge_y2])

        del camera
        return digitalMeasurement
