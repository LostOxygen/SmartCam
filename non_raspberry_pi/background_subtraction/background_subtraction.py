#!/usr/bin/env python3
# -*- coding: utf8 -*-

import cv2
import sys
import os
import numpy as np
import argparse
import configparser
from pathlib import Path
from matplotlib import pyplot as plt


def main(argv):
    filename = argv[0]
    filename2 = argv[1]
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    img2 = cv2.imread(filename2, cv2.IMREAD_COLOR)

    if img is None:
        print("Fehler bei Laden der Datei: " + filename + "!\n")
        return -1

    print(img.shape)
    print(img2.shape)
    result = cv2.subtract(img, img2)

    cv2.namedWindow("subtraction", 1)
    cv2.imshow("subtraction", result)
    cv2.waitKey(0)



if __name__ == "__main__":
    main(sys.argv[1:])
