#!/usr/bin/env python3

import socket
import sys
from KreisPi import Kreis
from configGenerator import Config
from camera_pi import Camera
import time
from datetime import datetime
import cv2
import os
import numpy as np
from PIL import Image
import io
import pprint #Debug

#------------ NeoPixel Config -----------
from neopixel import *
from rpi_ws281x import *
LED_COUNT = 16 #Anzahl LEDs
LED_PIN = 18 #GPIO Pin für LEDs
LED_FREQ_HZ = 800000 #Frequenz fürs Signal in Hz
LED_DMA = 10 #DMA Channel für Signal
LED_BRIGHTNESS = 255 #Helligkeit von 0 bis 255
LED_INVERT = False

# ------------ Netzwerk ----------------
#HOST = '192.168.8.60' #IP Adresse des RPI
HOST = '127.0.0.1'
PORT = 65432 #Port auf dem gehört wird

# ------------ Variablen ---------------
exit = False
camera = Camera() #erstellt Global eine Kamera
lichtwert = (0,0,0)


# ------------ Main Code ---------------

def make_picture(camera, fileName): #Funktion zum Bild erstellen
    if camera.get_frame is not None:
        ret, jpeg = cv2.imencode('.jpg', camera.get_frame_cv()) #dekodiert das RAW Image zu JPEG
        img2 = Image.open(io.BytesIO(jpeg.tobytes())) #konvertiert jpeg zu einem Byte Objekt um es mit BytesIO zu handhaben
        img2.save("/home/pi/Desktop/OpenCV/tcp_server/images/" + fileName) #speichert es als fileName ab
        return True
    else:
        print("Kamera Frame ist None")
        return False

#---------------------------- Beginn Server ------------------------------------------------------
def main():
    strip.begin()
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
                        break
#--------------------------------------------------------------------------------------------------
                    if data[0] == 'G' and data[1] == 'O': #Get Offset
                        try:
                            offset = Kreis.kreis(camera, False)
                            ausgabe = "GO" + "X" + str(offset[0]) + "Y" + str(offset[1]) + "\x00"
                        except Exception as e:
                            print("Fehler beim Offset erstellen!")
                            print(e)
                            ausgabe = "ER" + "\x00"

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

                        if make_picture(camera, fileName):
                            ausgabe = "OK" + "\x00"
                        else:
                            ausgabe = "NO" + "\x00"

                        ausgabe = ausgabe.encode()
                        conn.sendall(ausgabe)
#--------------------------------------------------------------------------------------------------
                    if data[0] == 'C' and data[1] == 'V': #erstellt bild mit kreis
                        try:
                            if Kreis.kreis(camera, True): #Kreis mit Image = True aufrufen
                                ausgabe = "OK" + "\x00"
                            else:
                                ausgabe = "NO" + "\x00"
                        except Exception as e:
                            print("Fehler beim erstellen eines Bildes mit Kreiserkennung")
                            print(e)
                            ausgabe = "ER" + "\x00"

                        ausgabe = ausgabe.encode()
                        conn.sendall(ausgabe)
#--------------------------------------------------------------------------------------------------
                    if data[0] == 'C' and data[1] == 'O': #configGenerator
                        ausgabe = "Server wird konfiguriert!" + "\x00"
                        ausgabe = ausgabe.encode()
                        conn.sendall(ausgabe)
                        try:
                            if Config.createConfig(camera):
                                ausgabe = "OK" + "\x00"
                            else:
                                ausgabe = "NO" + "\x00"
                            ausgabe = ausgabe.encode()
                            conn.sendall(ausgabe)
                        except Exception as e:
                            ausgabe = "ER" + "\x00"
                            print(e)
                            ausgabe = ausgabe.encode()
                            conn.sendall(ausgabe)
#--------------------------------------------------------------------------------------------------
                    if data[0] == 'E' and data[1] == 'X': #Exit und sendet EX als Exitcode
                        ausgabe = "EX" + "\x00"
                        print("Server wird beendet!")
                        exit = True
                        ausgabe = ausgabe.encode()
                        conn.sendall(ausgabe)
                        break
#--------------------------------------------------------------------------------------------------
                    if data[0] == 'F' and data[1] == 'X': #Licht
                        lichtwert = str(data[2]) + str(data[3]) + str(data[4]) #Hängt Daten aneinander
                        lichtwert = (int(lichtwert),int(lichtwert),int(lichtwert)) #speichert sie als INT Tripel ab
                        print("Licht wurde auf " + str(lichtwert) + " gesetzt.")

                        for i in range(0, strip.numPixels(), 1): #setzt alle Pixel auf 'Lichtwert'
                            strip.setPixelColor(i, Color(lichtwert))
                            strip.show()

                        ausgabe = "OK" + "\x00"
                        ausgabe = ausgabe.encode()
                        conn.sendall(ausgabe)
#--------------------------------------------------------------------------------------------------
            if exit == True:
                break
#------------------------------ Ende Server   -----------------------------------------------------


if __name__ == '__main__':
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    main()
