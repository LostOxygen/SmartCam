#!/usr/bin/env python3

import socket

HOST = '127.0.0.1' #IP Adresse des RPI
PORT = 65432 #Port des Servers

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST,PORT))
    while True:
        command = input("Befehl: ")
        command = command.encode()
        sock.sendall(command)
        data = sock.recv(1024)
        response = repr(data)
        print('Received Data: ', response)
        if str(response) == 'Ciao':
            break
print("Verbindung Beendet!")
