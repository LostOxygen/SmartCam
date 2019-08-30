#!/usr/bin/env python3
# -*- coding: utf8 -*-

import socket


HOST = input("IP eingeben: ")
PORT = 65432 #Port des Servers

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST,PORT))
    print("Befehle: \n EX : beendet Server und Verbindung \n GO : liefert Offset zurueck \n CFGx : konfiguriert die Kreiserkennung \n IM : erstellt ein einfaches Bild \n CV : erstellt ein Bild mit erkannten Kreisen \n FX123: setzt LED-Ring auf Farbwert 123,123,123 \n KOx: liefert Kabeloffset zurück \n")
    while True:
        command = input("Befehl: ")
        command = command.encode()
        sock.sendall(command)
        data = sock.recv(1024)
        response = data.decode()
        print('Empfangene Daten: ', response)

        if response[0] == 'E' and response[1] == 'X':
            print("Verbindung wird beendet..")
            break
print("Verbindung Beendet!")
