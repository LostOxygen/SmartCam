#!/usr/bin/env python3
# -*- coding: utf8 -*-
#montybot imports
import logging
from ..exceptions.exceptions import NoContoursFoundException, NoImageDataFoundException
from .geometry import Line_, Vector, Area
from ..configLoader import configReader

#general imports
import cv2
import sys
import numpy as np
import time
from datetime import datetime


class partDetection():
    clear = lambda: os.system('clear')
    windowName = "detection"
    gaussMatrix = (7,7)
    gaussFactor = 0
    lowerThreshold = 250
    upperThreshold = 300
    upperLeft = (0, 0)
    lowerRight = (1440, 1080)
    gripPointRadius = 30 #mm
    try:
        gripPointRadius = configReader.returnEntry('contours', 'grippointradius')
    except Exception as e:
        logging.debug(e)

# -------------------- constructor -----------------------------------------------------
    def __init__(cls):
        pass

# --------------------- returns a timestamp ---------------------------------------------
    @classmethod
    def getTimestamp(cls):
        d = datetime.now()
        imgYear = "%04d" % (d.year)
        imgMonth = "%02d" % (d.month)
        imgDate = "%02d" % (d.day)
        imgHour = "%02d" % (d.hour)
        imgMins = "%02d" % (d.minute)
        timestamp = "" + str(imgDate) + "." + str(imgMonth) + "." + str(imgYear) + " " + str(imgHour) + ":" + str(imgMins)

        return timestamp


# ------------------ saves the output image for debugging --------------------------------
    @classmethod
    def saveImg(cls, img):
        filename = "partDetection.jpg"
        cv2.imwrite("../images/" + filename, img)


# ------------------------- visualizes the detected parts etc. on the frame --------------------
    @classmethod
    def visuals(cls, img, contours, box, innerBox, gripPoint, gripArea):
        cv2.putText(img, cls.getTimestamp(), (10, 725), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2, cv2.LINE_AA, 0)
        cv2.drawContours(img, [box], -1, (0,255,0), 3)
        cv2.circle(img, gripPoint, cls.gripPointRadius,(255,0,0), 2)
        cv2.drawContours(img, [gripArea], -1, (255,0,0), 3)
        if innerBox is not None:
            cv2.drawContours(img, [innerBox], -1, (0,0,255), 3)



# ----------------- returns contours of the detected part -----------------------------
    @classmethod
    def getContours(cls, img):
        contours, hierarchy = cv2.findContours(img, 1, 2)
        cnt = contours[0]
        area = cv2.contourArea(cnt)
        for cntTemp in contours:
            areaTemp = cv2.contourArea(cntTemp)
            if areaTemp > area:
                area = areaTemp
                cnt = cntTemp

        logging.debug("selected area: " + str(area))
        approx = cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True)
        hull = cv2.convexHull(cnt)

        rect = cv2.minAreaRect(cnt)
        rect = ((rect[0][0] + cls.upperLeft[0], rect[0][1] + cls.upperLeft[1]), rect[1], rect[2])
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        return rect, contours, box, area


# --------------------------- sorts the points to identify which point belongs to which corner -----
    @classmethod
    def sortPoints(cls, box):
        xValues = box[:,0]
        yValues = box[:,1]
        ind = np.argsort(xValues)
        X, Y = xValues[ind], yValues[ind]

        xLeftSide = np.array([X[0], X[1]])
        xRightSide = np.array([X[2], X[3]])

        yLeftSide = np.array([Y[0], Y[1]])
        yRightSide = np.array([Y[2], Y[3]])

        indLeft = np.argsort(yLeftSide)
        xLeftSide, yLeftSide = xLeftSide[indLeft], yLeftSide[indLeft]

        indRight = np.argsort(yRightSide)
        xRightSide, yRightSide = xRightSide[indRight], yRightSide[indRight]

        upLeft = np.array([xLeftSide[0], yLeftSide[0]])
        upRight = np.array([xRightSide[0], yRightSide[0]])
        downLeft = np.array([xLeftSide[1], yLeftSide[1]])
        downRight = np.array([xRightSide[1], yRightSide[1]])

        sortedBox = np.array([upLeft, upRight, downLeft, downRight])

        return sortedBox


# ---------------- returns the outer box points ----------------------------------------
    @classmethod
    def getBoxPoints(cls, box):
        xValues = box[:,0]
        yValues = box[:,1]

        points = [[min(xValues), min(yValues)], [min(xValues), max(yValues)], [max(xValues), min(yValues)], [max(xValues), max(yValues)]]

        return points


# ---------------- returns the offset tupel (X, Y) ----------------------------------------
    @classmethod
    def getOffset(cls, gripPoint):
        mmPerPixel = 1#configReader.returnEntry((('contours', 'mmPerPixel')))
        mittelpunkt = (int(cls.upperLeft[0]+(cls.lowerRight[0]-cls.upperLeft[0])/2), int(cls.upperLeft[1]+(cls.lowerRight[1]-cls.upperLeft[1])/2))

        offset = (mittelpunkt[0] - gripPoint[0] , mittelpunkt[1] - gripPoint[1])
        offset = (round((offset[0]*mmPerPixel),2), round((offset[1]*mmPerPixel),2))

        logging.info("Offset:" + str(offset))
        return offset


# ---------------- calculates the center of a box ------------------------------ ------------
    @classmethod
    def calculateCenter(cls, box):
        box = cls.sortPoints(box)

        Line1 = Line_(Vector(box[0][0], box[0][1]), Vector(box[3][0], box[3][1]))
        Line2 = Line_(Vector(box[1][0], box[1][1]), Vector(box[2][0], box[2][1]))

        intersection = Line1.intersection(Line2)

        center = (int(np.round(intersection.x)), int(np.round(intersection.y)))
        logging.info("calculated center: " + str(center))
        return center


# ---------------- calculates offset for grip_point to avoid intersections ---------------------
    @classmethod
    def calculateGripPoint(cls, gripPoint, innerBox, gripArea):
        if Area.intersection(gripPoint, innerBox, gripArea):
            logging.info("Intersection between GripPoint and hole detected")
        else:
            logging.info("No GripPoint intersections detected")

        return gripPoint


# ------------------------- calculates rotation offset ------------------------------
    @classmethod
    def getRotation(cls, gripPoint, box):
        box = cls.sortPoints(box)
        boxVector = Vector(box[1][0]-box[0][0], box[1][1]-box[0][1]) #vector of the top box contour
        gripPointVector = Vector(gripPoint[0]-box[0][0], 0)
        logging.info("boxVector:" + str((boxVector.x, boxVector.y)))
        logging.info("gripPointVector:" + str((gripPointVector.x, gripPointVector.y)))

        rotation = boxVector.angle(gripPointVector)
        logging.info("rotation offset:" + str(rotation))

        return rotation


# ------------------------- calculates contours of holes in the part ------------------------------
    @classmethod
    def getInnerContours(cls, extract, box, outerArea):
        points = cls.getBoxPoints(box)

        upLeft = points[0]
        downRight = points[3]

        extract_width_height = extract.shape[0] * extract.shape[1]

        logging.debug("Search for contours in area: " + str(upLeft) + " to " + str(downRight))
        extract = extract[upLeft[1] : downRight[1], upLeft[0] : downRight[0]]

        extract_width_height2 = extract.shape[0] * extract.shape[1]

        factor = extract_width_height2 / extract_width_height
        logging.debug("factor: " + str(factor))

        contours, hierarchy = cv2.findContours(extract, 1, 2)
        if len(contours) > 0:
            cnt = contours[0]
            area = cv2.contourArea(cnt)
            for cntTemp in contours:
                areaTemp = cv2.contourArea(cntTemp)
                if areaTemp > area and areaTemp < (outerArea/2):
                    area = areaTemp
                    cnt = cntTemp

            logging.debug("areaTemp: " + str(area) + " outerArea: " + str(outerArea))
            approx = cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True)
            hull = cv2.convexHull(cnt)

            rect = cv2.minAreaRect(cnt)
            rect = ((rect[0][0] + upLeft[0], rect[0][1] + upLeft[1]), rect[1], rect[2])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
        else:
            raise NoContoursFoundException("could not find any inner Contours!")

        return rect, box, extract


# ---------------- main procedure to start calculations for part detection -----------------------------
    @classmethod
    def detectParts(cls, boxHasHole=False):
        from picamera import PiCamera
        from picamera.array import PiRGBArray
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

        if img is None:
            raise NoImageDataFoundException(filename)
            return -1

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grayFiltered = cv2.GaussianBlur(gray, cls.gaussMatrix, cls.gaussFactor)

        _, threshold  = cv2.threshold(grayFiltered, 120, 255, cv2.THRESH_TOZERO)
        canny = cv2.Canny(threshold, cls.lowerThreshold, cls.upperThreshold)

        outerRect, contours, box, outerArea = cls.getContours(canny[cls.upperLeft[1] : cls.lowerRight[1], cls.upperLeft[0] : cls.lowerRight[0]])
        #rect is defined as ((center_x, center_y), (width, height), angle_of_rotation)

        gripPoint = cls.calculateCenter(box)

        gripArea = np.array([
            (gripPoint[0]-cls.gripPointRadius, gripPoint[1]-cls.gripPointRadius), (gripPoint[0]+cls.gripPointRadius, gripPoint[1]-cls.gripPointRadius), (gripPoint[0]+cls.gripPointRadius, gripPoint[1]+cls.gripPointRadius),
            (gripPoint[0]-cls.gripPointRadius, gripPoint[1]+cls.gripPointRadius)
            ])

        if boxHasHole:
            innerRect, innerBox, extract = cls.getInnerContours(canny, box, outerArea)
            gripPoint = cls.calculateGripPoint(gripPoint, innerBox, gripArea)
        else:
            innerBox = None

        offset = cls.getOffset(gripPoint)
        rotation = cls.getRotation(gripPoint, box)

        cls.visuals(img, contours, box, innerBox, gripPoint, gripArea)
        cls.saveImg(img)

        return offset, rotation




if __name__ == "__main__":
    partDetection.detectParts(sys.argv[1:])
