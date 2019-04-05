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

# ------------ Netzwerk ----------------
#HOST = '192.168.8.60' #IP Adresse des RPI
HOST = '127.0.0.1'
PORT = 65432 #Port auf dem gehört wird

# ------------ Variablen ---------------
exit = False
camera = Camera()
# ------------ Main Code ---------------

def make_picture(camera, fileName):
    if camera.get_frame is not None:
        img2 = Image.open(io.BytesIO(camera.get_frame())) #lädt frame als ByteIO um es zu öffnen
        img2.save("/home/pi/Desktop/OpenCV/tcp_server/images/" + fileName) #speichert es als fileName ab
        return True
    else:
        print("Kamera Frame ist None")
        return False

def main():
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
                        #camera = Camera()

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

                        #del camera
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
                        if Config.createConfig == True: #Überprüft ob config generiert wurde
                            succ = "Config wurde generiert!" + "\x00"
                            succ = succ.encode()
                            conn.sendall(succ)
                        else:
                            err = "Config konnte nicht erstellt werden!" + "\x00"
                            err = err.encode()
                            conn.sendall(err)
#--------------------------------------------------------------------------------------------------
                    if data[0] == 'E' and data[1] == 'X': #Exit und sendet EX als Exitcode
                        ausgabe = "EX" + "\x00"
                        print("Server wird beendet!")
                        exit = True
                        ausgabe = ausgabe.encode()
                        conn.sendall(ausgabe)
                        break

            if exit == True:
                break

if __name__ == '__main__':
    main()
