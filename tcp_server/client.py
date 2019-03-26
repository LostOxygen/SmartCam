#!/usr/bin/env python3

import socket

HOST = '127.0.0.1' #IP Adresse des RPI / Servers
PORT = 65432 #Port des Servers

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST,PORT))
    print("Befehle: \n EX : beendet Server und Verbindung \n GO : liefert Offset zurueck \n CO : konfiguriert die Kreiserkennung")
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
