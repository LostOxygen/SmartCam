#!/usr/bin/env python3
# -*- coding: utf8 -*-

#import socket
import sys
#from KreisPi import Kreis
#from kabel import Kabel
#from configGenerator import Config
#from camera_pi import Camera
import time
#from datetime import datetime
#import cv2
#import os
#import numpy as np
#from PIL import Image
import io
#import linecache
import requests
#import configparser
#import traceback
#from pathlib import Path
#import pprint #Debug
import struct

class Gripper:
	def __init__(self):
		self._baseuri = 'http://192.168.8.240'

	def _build_value(self, exec, cmd, force, pos):
		# force: 0 = 100%, 1 = 75%, 2 = 50%, 3 = 25%
		ba = bytearray(struct.pack("f", pos))
		byte0 = exec << 7 | cmd
		value = "%02X%02X%02X%02X%02X%02X%02X%02X" % (byte0, 0, force, 0, ba[3], ba[2], ba[1], ba[0])
		return value

	def send_request(self, cmd, force, pos):
		value = self._build_value(0, cmd, force, pos)
		r = requests.post(self._baseuri, json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[1]/iolinkdevice/pdout/setdata", "data":{"newvalue":value}})
		value = self._build_value(1, cmd, force, pos)
		r = requests.post(self._baseuri, json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[1]/iolinkdevice/pdout/setdata", "data":{"newvalue":value}})
		

# 8 bit Befehlt
# 0x00 (Werkstückträgernummer)
# 0x00 (Greifkraft)
# 0x00 RFU
# 4 Byte Zielposition

# quittieren
#r = requests.post('http://192.168.8.240', json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[1]/iolinkdevice/pdout/setdata", "data":{"newvalue":"0100000000000000"}})
#r = requests.post('http://192.168.8.240', json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[1]/iolinkdevice/pdout/setdata", "data":{"newvalue":"8100000000000000"}})


# greifen
#r = requests.post('http://192.168.8.240', json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[1]/iolinkdevice/pdout/setdata", "data":{"newvalue":"0400000000000000"}})
#r = requests.post('http://192.168.8.240', json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[1]/iolinkdevice/pdout/setdata", "data":{"newvalue":"8400000000000000"}})


