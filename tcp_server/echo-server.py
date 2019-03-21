#!/usr/bin/env python3

import socket

HOST = '127.0.0.1' #IP Adresse des RPI
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST,PORT))
    sock.listen()
    conn, addr = sock.accept()
    with conn:
        print('Connected by: ', addr)
        while True:
            data = conn.recv(1024)
            data = data.decode()
            if not data:
                pass

            if str(data) == 'test':
                ausgabe1 = 'Hallo'
                ausgabe1 = ausgabe1.encode()
                conn.sendall(ausgabe1)

            if str(data) == 'exit':
                ausgabe2 = 'Ciao'
                ausgabe2 = ausgabe2.encode()
                conn.sendall(ausgabe2)
                break
