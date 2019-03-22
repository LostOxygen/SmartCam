#!/usr/bin/env python3

import socket

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
                if not data:
                    #print('Warte auf Daten..')
                    break

                if str(data) == 'test':
                    ausgabe1 = 'Hallo'
                    ausgabe1 = ausgabe1.encode() #wieder in binär kodieren
                    conn.sendall(ausgabe1)

                if str(data) == 'exit':
                    ausgabe2 = 'Ciao'
                    ausgabe2 = ausgabe2.encode()
                    conn.sendall(ausgabe2)
                    break

                else:
                    ausgabe = str(data)
                    laenge = len(str(data))
                    ausgabe3 = "Nachricht: " + ausgabe + " mit Laenge: " + str(laenge)
                    ausgabe3 = ausgabe3.encode()
                    conn.sendall(ausgabe3)
