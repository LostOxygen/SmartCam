#!/usr/bin/python3

##########################
# Author: Jonathan Evertz
# Date: 21.2.2019
# Version: 1.0
# Generator für OpenCV Config File
##########################

import cv2
import sys
import os
import numpy as np
import argparse
import math
import configparser
from pathlib import Path
from pprint import pprint #nur für Debug benötigt

config = configparser.ConfigParser()
test = 30
config['KREISERKENNUNG'] = {'AbstandZumObjekt' : '15', 'DurchmesserKreisInPixel' : test}

with open('config.ini', 'w') as configfile:
    config.write(configfile)
