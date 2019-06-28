#!/usr/bin/env python3
# -*- coding: utf8 -*-

import socket
import sys
from KreisPi import Kreis
from kabel import Kabel
from configGenerator import Config
from camera_pi import Camera
import time
from datetime import datetime
import cv2
import os
import numpy as np
from PIL import Image
import io
import linecache
import requests
import configparser
from pathlib import Path
import pprint #Debug

#------------ NeoPixel Config -----------
#from neopixel import *
LED_COUNT = 16 #Anzahl LEDs
LED_PIN = 18 #GPIO Pin für LEDs
LED_FREQ_HZ = 800000 #Frequenz fürs Signal in Hz
LED_DMA = 10 #DMA Channel für Signal
LED_BRIGHTNESS = 255 #Helligkeit von 0 bis 255
LED_INVERT = False
LED_CHANNEL = 5

# ------------ Netzwerk ----------------
#HOST = '192.168.8.60' #IP Adresse des RPI1
#HOST = '192.168.8.65' #IP Adresse des RPI2
HOST = '127.0.0.1' #Standard HOST wenn in der Config nichts steht
PORT = 65432 #Port auf dem gehört wird (Standard)

# ------------ Variablen ---------------
exit = False
camera = Camera() #erstellt Global eine Kamera
lichtwert = (0,0,0)
config_test = True #zum Abfragen der Config
# ------------ Debug Funktionen --------
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('Exception in ({}, Line: {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

# ------------ Main Code ---------------

def make_picture(camera, fileName): #Funktion zum Bild erstellen
    if camera.get_frame is not None:
        ret, jpeg = cv2.imencode('.jpg', camera.get_frame_cv()) #dekodiert das RAW Image zu JPEG
        img2 = Image.open(io.BytesIO(jpeg.tobytes())) #konvertiert jpeg zu einem Byte Objekt um es mit BytesIO zu handhaben
        img2.save("/home/pi/Desktop/OpenCV/raspberry_pi/bilder/" + fileName) #speichert es als fileName ab
        return True
    else:
        print("Kamera Frame ist None")
        return False

#---------------------------- Beginn Server ------------------------------------------------------
def main():
    print("Befehle: \n EX : beendet Server und Verbindung \n GO : liefert Offset zurueck \n CFGx : konfiguriert die Kreiserkennung \n IM : erstellt ein einfaches Bild \n CV : erstellt ein Bild mit erkannten Kreisen \n FX123: setzt LED-Ring auf Farbwert 123,123,123 \n KOx: liefert Kabeloffset zurück \n")
    #strip.begin()
    print("Hostet Server auf: " + HOST + " auf Port: " + str(PORT))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #AF_INET = Inet Adress Family (IPv4), SOCK_STREAM = socket type (TCP)
        sock.bind((HOST,PORT))
        sock.listen()
        while True:
            conn, addr = sock.accept()
            with conn:
                print('Connected by: ', addr)
                while True:
                    data = conn.recv(1024) #empfängt Daten der Verbindung (max 1024 Byte)
                    data = data.decode() #Dekodiert, weil Binär
                    data = str(data) #Data zu String konvertieren
#--------------------------------------------------------------------------------------------------
                    if not data: #Guckt ob überhaupt Daten kommen
                        conn.close()
                        break
#--------------------------------------------------------------------------------------------------
                    if data[0] == 'G' and data[1] == 'O': #Get Offset
                        try:
                            offset = Kreis.kreis(camera, False)
                            ausgabe = "GO" + "X" + str(offset[0]) + "Y" + str(offset[1]) + "\x00"
                        except Exception as e:
                            print("Fehler beim Offset erstellen!")
                            print(e)
                            PrintException()
                            ausgabe = "NAK" + "\x00"

                        ausgabe = ausgabe.encode()
                        conn.sendall(ausgabe)

#--------------------------------------------------------------------------------------------------
                    if data[0] == 'K' and data[1] == 'O': #Get Kabeloffset
                        try:
                            offset = Kabel.kabel(camera, data[2])
                            ausgabe = "KO" + "X" + str(offset[0]) + "Y" + str(offset[1]) + "\x00"
                        except Exception as e:
                            print("Fehler beim Offset erstellen!")
                            print(e)
                            PrintException()
                            ausgabe = "NAK" + "\x00"

                        ausgabe = ausgabe.encode()
                        conn.sendall(ausgabe)

#--------------------------------------------------------------------------------------------------
                    if data[0] == 'I' and data[1] == 'M': #erstellt einfaches Bild

                        d = datetime.now()
                        imgYear = "%04d" % (d.year)
                        imgMonth = "%02d" % (d.month)
                        imgDate = "%02d" % (d.day)
                        imgHour = "%02d" % (d.hour)
                        imgMins = "%02d" % (d.minute)
                        #Todo Sekunde programmieren
                        fileName = "" +str(imgYear) + str(imgMonth) + str(imgDate) + str(imgHour) + str(imgMins) + ".jpg"
                        try:
                            make_picture(camera, fileName)
                            ausgabe = "ACK" + "\x00"
                        except Exception as e:
                            print(e)
                            PrintException()
                            ausgabe = "NAK" + "\x00"

                        ausgabe = ausgabe.encode()
                        conn.sendall(ausgabe)
#--------------------------------------------------------------------------------------------------
                    if data[0] == 'C' and data[1] == 'V': #erstellt bild mit kreis
                        try:
                            if Kreis.kreis(camera, True): #Kreis mit Image = True aufrufen
                                ausgabe = "ACK" + "\x00"
                            else:
                                ausgabe = "NAK" + "\x00"
                        except Exception as e:
                            print("Fehler beim erstellen eines Bildes mit Kreiserkennung")
                            print(e)
                            PrintException()
                            ausgabe = "NAK" + "\x00"

                        ausgabe = ausgabe.encode()
                        conn.sendall(ausgabe)
#--------------------------------------------------------------------------------------------------
                    if data[0] == 'C' and data[1] == 'F' and data[2] == 'G': #configGenerator
                        ausgabe = "Server wird konfiguriert!" + "\x00"
                        ausgabe = ausgabe.encode()
                        try:
                            hoehe = int(data[3] + data[4] + data[5])
                            Config.createConfig(camera, data[6], hoehe)
                            ausgabe = "ACK" + "\x00"

                            ausgabe = ausgabe.encode()
                            conn.sendall(ausgabe)
                        except Exception as e:
                            ausgabe = "NAK" + "\x00"
                            print(e)
                            PrintException()
                            ausgabe = ausgabe.encode()
                            conn.sendall(ausgabe)
#--------------------------------------------------------------------------------------------------
                    if data[0] == 'E' and data[1] == 'X': #Exit und sendet EX als Exitcode
                        ausgabe = "EX" + "\x00"
                        print("Server wird beendet!")
                        exit = True
                        ausgabe = ausgabe.encode()
                        conn.sendall(ausgabe)
                        return 0
#--------------------------------------------------------------------------------------------------
                    if data[0] == 'F' and data[1] == 'X': #Licht
                        color = str(data[2]) + str(data[3]) + str(data[4]) + str(data[5]) + str(data[6]) + str(data[7])

                        cmd = '/home/pi/led.py ' + color
                        os.system(cmd)
                        ausgabe = "ACK"
                        ausgabe = ausgabe.encode()
                        conn.sendall(ausgabe)
#--------------------------------------------------------------------------------------------------
                    if data[0] == 'G' and data[1] == 'A' and data[2] == '0':
                        r = requests.post('http://192.168.8.240', json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[1]/iolinkdevice/pdout/setdata", "data":{"newvalue":"00"}})
                        r = requests.post('http://192.168.8.240', json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[2]/iolinkdevice/pdout/setdata", "data":{"newvalue":"01"}})
                    if data[0] == 'G' and data[1] == 'A' and data[2] == '1':
                        r = requests.post('http://192.168.8.240', json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[2]/iolinkdevice/pdout/setdata", "data":{"newvalue":"00"}})
                        r = requests.post('http://192.168.8.240', json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[1]/iolinkdevice/pdout/setdata", "data":{"newvalue":"01"}})
                    if data[0] == 'G' and data[1] == 'B' and data[2] == '0':
                        r = requests.post('http://192.168.8.240', json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[3]/iolinkdevice/pdout/setdata", "data":{"newvalue":"00"}})
                        r = requests.post('http://192.168.8.240', json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[4]/iolinkdevice/pdout/setdata", "data":{"newvalue":"01"}})
                    if data[0] == 'G' and data[1] == 'B' and data[2] == '1':
                        r = requests.post('http://192.168.8.240', json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[4]/iolinkdevice/pdout/setdata", "data":{"newvalue":"00"}})
                        r = requests.post('http://192.168.8.240', json={"code":"request", "cid":4711, "adr":"iolinkmaster/port[3]/iolinkdevice/pdout/setdata", "data":{"newvalue":"01"}})

#------------------------------ Ende Server   -----------------------------------------------------


if __name__ == '__main__':
# ----------- Pfade überprüfen ----------------------------------------
    if os.path.isdir('home/pi/OpenCV/raspberry_pi/bilder'):
        pass
    else:
        os.system('mkdir /home/pi/OpenCV/raspberry_pi/bilder')

# ----------- Config einlesen und überprüfen --------------------------
    config = configparser.ConfigParser()
    test = Path('../config.ini')
    if test.is_file():
        print('Config Datei gefunden')
        config.read('../config.ini')
        config_test = True

    else:
        print('Config konnte nicht gefunden werden. Bitte erst mit configGenerator.py eine Config generieren lassen und dann den Server neustarten!')
        config_test = False

    if config_test:
        HOST = config['CONFIG']['host']
        PORT = int(config['CONFIG']['port'])
# ---------------------------------------------------------------------

    main()
