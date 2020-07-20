#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import socket

'''
just a simple testclient to send data to a specific address.
Usage: 'python3 testClient.py <ip-address>' or just 'python3 testClient.py' and enter the address when asked to
'''

def main(argv):
    try:
        HOST = argv[0]
    except Exception as e:
        print(e)
        HOST = input("Enter IP address: ")

    PORT = 5005 #server port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST,PORT))
        while True:
            command = input("Command: ")
            command = command.encode()
            sock.sendall(command)
            data = sock.recv(1024)
            response = data.decode()
            print('Received data: ', response)

            if len(response) == 2 and response[0] == 'E' and response[1] == 'X':
                print("Closing connection..")
                break

    print("Connection closed!")

if __name__ == "__main__":
    main(sys.argv[1:])
