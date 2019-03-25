#!/usr/bin/env python3

import socket
from KreisPi import Kreis
import pprint

HOST = '192.168.8.60' #IP Adresse des RPI
PORT = 65432 #Port auf dem gehört wird

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

                if not data:
                    #print('Warte auf Daten..')
                    break

                if data == 'test':
                    ausgabe1 = 'Hallo'
                    ausgabe1 = ausgabe1.encode() #wieder in binär kodieren
                    conn.sendall(ausgabe1)

                if data == 'exit':
                    ausgabe2 = 'Ciao'
                    ausgabe2 = ausgabe2.encode()
                    conn.sendall(ausgabe2)
                    break

                if data[0] == 'G' and data[1] == 'O':
                    offset = Kreis.kreis()
                    ausgabe = "GO" + "X" + str(offset[0]) + "Y" + str(offset[1]) + "\x00"
                    ausgabe = ausgabe.encode()
                    conn.sendall(ausgabe)
