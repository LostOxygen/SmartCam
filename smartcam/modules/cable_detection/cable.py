#!/usr/bin/env python3
# -*- coding: utf8 -*-

import logging
import cv2
import sys
import os
import numpy as np
from ...core.configLoader import configReader
from pathlib import Path
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import io
from datetime import datetime
import imutils

class cableDetection():
'''
This class takes a picture with the RPI Camera and looks for the top of a cable and calculates its offset and angle relatively to the center of the image (where the robot gripper is supposed to be)
'''
    def __init__(cls):
        pass

    fenster_name = "Cable Detection"
    detection_size = (500, 500)
    config_test = True
    umrechnung_pixel_mm = 1 #to avoid errors the value is preset to 1
    maxCorners = 300 #amount of detection points
    qualityLevel = 0.03 #higher value is more accurate
    minDistance = 10 #minimum distance between points

    @classmethod
    def visualization_rgb(cls, img, min_xy, height, mittelpunkt, dist_x_mm, dist_y_mm, dist_x, dist_y):
    #visualization of the rgb picture
        cv2.line(img, min_xy, (min_xy[0], int(height/2)), (255,255,255), 2)
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
        #visualization of the gray picture
        cv2.line(gray, extLeft, (extLeft[0], int(g_height/2)), (255,255,255), 2)
        cv2.circle(gray, g_mittelpunkt, 2, (255,255,255), 2)
        cv2.line(gray, g_mittelpunkt, (extLeft[0], int(g_height/2)), (255,255,255), 2)
        cv2.line(gray, g_mittelpunkt, extLeft, (255,255,255), 2)

    @classmethod
    def saveImg(cls, bild_num, img, gray):
        # saves the image in the path which is specified in the config file
        path = configReader.returnEntry("options", "imagepath")
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except Exception as e:
                logging.error("Image directory couldn't get created.. \n" + str(e))

        logging.debug("saved cable.jpg and cablegray.jpg in " + path)
        cv2.imwrite(path + str(bild_num)+".jpg", gray)
        cv2.imwrite(path + str(bild_num)+".jpg", img)

    @classmethod
    def removeBackground(cls, img, background):
        # removes the background by checking if it's difference is smaller than a threshold
        result = np.copy(img)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                diff = img[i][j] - background[i][j]
                if diff < 100:
                    result[i][j] = 255

        return result

    @classmethod
    def config(cls):
        cls.umrechnung_pixel_mm = float(configReader.returnEntry('conversion', 'mm_per_pixel'))

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
        # main part which checks first initializes the PiCamera and takes a picture and then looks for wires and their angle
        cls.config()
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
        if img is None: #to prevent errors with empty images
            logging.error("Could not load frame properly..")
            return -1

        height, width = img.shape[:2] # image shape has 3 dimensions
        # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape
        mittelpunkt = (int(width/2), int(height/2))
        img = cls.rotate(img, mittelpunkt, width, height)

        try:
            background = cv2.imread('~/.smartcam/background.jpg', 2)
            background = cls.rotate(background, mittelpunkt, width, height) #rotates background
        except Exception as e:
            logging.info("Background couldn't get loaded. Background removal disabled..")

        height, width = img.shape[:2]
        oben_links = (int(mittelpunkt[0]- cls.detection_size[0]), int(mittelpunkt[1]- cls.detection_size[1]/2))
        unten_rechts = (int(mittelpunkt[0]), int(mittelpunkt[1]+ cls.detection_size[1]/2))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if img.shape[0] == background.shape[0] and img.shape[1] == background.shape[1]:
            gray = cls.removeBackground(gray, background)
        else:
            logging.error("Background got wrong dimensions. Background removal disabled..")

        # crops the image to it's relevant areas
        gray = gray[int(oben_links[1]) : int(unten_rechts[1]), int(oben_links[0]) : int(unten_rechts[0])]
        blur = cv2.GaussianBlur(gray, (7,7), 1)
        blur = cv2.bilateralFilter(blur, 11, 17, 17)
        blur = cv2.Canny(blur, 30, 120)

        # search for contours and draw them
        contours = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(gray, contours[0], -1, (0,255,0), 3)

        # make a list out of the contours to sort them to detect the top of the cable
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

        min_xy = extLeft

        # calculating the offset between the center of the image (where the gripper is supposed to be) and the top of the wire
        dist_y = g_mittelpunkt[1] - min_xy[1]
        dist_x = g_mittelpunkt[0] - min_xy[0]
        min_xy = (int(mittelpunkt[0] - dist_x), int(mittelpunkt[1] - dist_y))
        dist_y_mm = (dist_y * cls.umrechnung_pixel_mm)/2
        dist_x_mm = (dist_x * cls.umrechnung_pixel_mm)/2

        cls.visualization_rgb(img, min_xy, height, mittelpunkt, dist_x_mm, dist_y_mm, dist_x, dist_y)

        cls.saveImg(bild_num, img, gray)
        offset = (round(dist_x_mm, 2), round(dist_y_mm, 2))

        return offset
