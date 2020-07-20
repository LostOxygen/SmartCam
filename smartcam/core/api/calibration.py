#!/usr/bin/env python3
# -*- coding: utf8 -*-
import logging
import time
import cv2
import sys
import numpy as np
from ..configLoader import configReader
from picamera.array import PiRGBArray
from picamera import PiCamera
import math
import os
from datetime import datetime

class calibration:
    min_threshold = 0
    max_threshold = 100
    kernel = np.ones((5, 5), np.uint8)
    gauss_faktor = 0
    gauss_matrix = (7,7)
    maxCorners = 300 #amount of detection points
    qualityLevel = 0.03 #higher is more accurate
    minDistance = 10 #min distance between points

    def __init__(cls):
        pass


    @classmethod
    def calibrate(cls):
        try:
            cls.realMeasurement = configReader.returnEntry("calibration", "realMeasurement")
        except Exception as e:
            cls.realMeasurement = 70
            logging.warning("Couldn't get realMeasurement data from config file.. \n" + str(e))

        digitalMeasurement = cls.scan()

        cls.mmPerPixel =  float(float(cls.realMeasurement) / float(digitalMeasurement))
        logging.info("calibration successful. Calibration Data: " + str(cls.mmPerPixel) + "mm per pixel")

        try:
            configReader.updateConfig("calibration", "mmPerPixel", cls.mmPerPixel)
        except Exception as e:
            logging.warning("Couldn't update config properly .. \n" + str(e))

    @classmethod
    def visualization(cls, img, points):
        cv2.circle(img, points[0], 2, (255,255,0), 2) #oben links
        cv2.circle(img, points[1], 2, (255,255,0), 2) #oben rechts
        cv2.circle(img, points[2], 2, (255,255,0), 2) #unten links
        cv2.circle(img, points[3], 2, (255,255,0), 2) #unten rechts
        timestamp = cls.getTimestamp()
        cv2.putText(img, timestamp, (20, 1060), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 2, cv2.LINE_AA, 0)

        return img

    @classmethod
    def getTimestamp(cls):
        d = datetime.now()
        imgYear = "%04d" % (d.year)
        imgMonth = "%02d" % (d.month)
        imgDate = "%02d" % (d.day)
        imgHour = "%02d" % (d.hour)
        imgMins = "%02d" % (d.minute)
        imgSecs = "%02d" % (d.second)
        timestamp = "" + str(imgDate) + "." + str(imgMonth) + "." + str(imgYear) + " " + str(imgHour) + ":" + str(imgMins) + ":" + str(imgSecs)
        return timestamp

    @classmethod
    def scan(cls):
        camera = PiCamera()
        camera.resolution = (1920, 1088)
        camera.hflip = True
        camera.vflip = True
        digitalMeasurement = 1

        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        img = rawCapture.array
        camera.close()
        del camera
        del rawCapture

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

            approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)

            x_values = []
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

            img = cls.visualization(img, points)
            cls.saveImg(img)
        return digitalMeasurement

    @classmethod
    def makeNormalImage(cls, imgName="normal_image", info=True):
        camera = PiCamera()
        camera.resolution = (1920, 1088)
        camera.hflip = True
        camera.vflip = True
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        img = rawCapture.array
        camera.close()
        del camera
        del rawCapture

        if info == True:
            cv2.putText(img, cls.getTimestamp(), (10, 725), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA, 0)

        if img is None:
            logging.warning("Could not load frame!" + "!\n")
            return -1

        path = configReader.returnEntry("options", "imagepath")
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except Exception as e:
                logging.error("Image directory couldn't get created.. \n" + str(e))

        logging.debug("saved " + imgName + " in " + path)
        cv2.imwrite(path + imgName, img)

        return "Image saved"

    @classmethod
    def saveImg(cls, img):
        path = configReader.returnEntry("options", "imagepath")
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except Exception as e:
                logging.error("Image directory couldn't get created.. \n" + str(e))

        logging.debug("saved quadrat.jpg in " + path)
        cv2.imwrite(path + "quadrat.jpg", img)

    @classmethod
    def writeText(cls, text, pos):
        image_path = configReader.returnEntry("options", "imagepath")
        image_list = ['quadrat.jpg', 'partDetection.jpg', 'cablegray1.jpg', 'cablegray2.jpg', 'circle.jpg']

        position = (0, 0)
        if pos == "ul":
            position = (200, 200)
        if pos == "dl":
            position = (200, 1200)
        if pos == "ur":
            position = (1200, 200)
        if pos == "dr":
            position = (1200, 1200)

        for img in image_list:
            path = image_path + img
            try:
                img = cv2.imread(path, cv2.IMREAD_COLOR)
                cv2.putText(img, text, position, cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA, 0)
                cv2.imwrite(path, img)

            except Exception as e:
                logging.error(str(e))
