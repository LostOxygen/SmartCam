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
	def __init__(self, port):
		self._baseuri = 'http://192.168.8.240'
		self._port = port

	def ack(self):
		self.send_request(0x01, 0, 0)

	def close(self, force=0):
		self.send_request(0x04, force, 0)

	def open(self, force=0):
		self.send_request(0x03, force, 0)

	def move_abs(self, pos, force=0):
		self.send_request(0x05, force, pos)

	def move_rel(self, dist):
		self.send_request(0x06, force, dist)

	def reference(self):
		self.send_request(0x02, 0, 0)

	def measure(self):
		self.send_request(0x07, 0, 0)

	def _build_value(self, exec, cmd, force, pos):
		# force: 0 = 100%, 1 = 75%, 2 = 50%, 3 = 25%
		ba = bytearray(struct.pack("f", pos))
		byte0 = exec << 7 | cmd
		value = "%02X%02X%02X%02X%02X%02X%02X%02X" % (byte0, 0, force, 0, ba[3], ba[2], ba[1], ba[0])
		return value

	def send_request(self, cmd, force, pos):
		adr = "iolinkmaster/port[%d]/iolinkdevice/pdout/setdata" % (self._port)
		value = self._build_value(0, cmd, force, pos)
		r = requests.post(self._baseuri, json={"code":"request", "cid":4711, "adr":adr, "data":{"newvalue":value}})
		value = self._build_value(1, cmd, force, pos)
		r = requests.post(self._baseuri, json={"code":"request", "cid":4711, "adr":adr, "data":{"newvalue":value}})
		#r = requests.post(self._baseuri, json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[1]/iolinkdevice/pdout/setdata", "data":{"newvalue":value}})
	
