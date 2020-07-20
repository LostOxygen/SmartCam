import logging
import socket

TIMEOUT = 5

class Server():
'''
Standard python implementation of a tcp/ip server without big changes.
'''

    BUFFER_SIZE = 1024

    def __init__(self, bind_ip=None, port=None):
        if bind_ip is None:
            bind_ip = "0.0.0.0"
        if port is None:
            port = 5005

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((bind_ip, port))
        self.s.settimeout(TIMEOUT)
        self.s.listen(True)
        self.conn = None
        logging.info("Server has been started.")


    def accept(self):
        try:
            self.conn, self.addr = self.s.accept()
            self.conn.settimeout(TIMEOUT)
            logging.info("Connection address: " + str(self.addr))
        except socket.timeout:
            self.conn = None


    def isConnected(self):
        return self.conn is not None


    def receive(self):
        if self.conn is None:
            return None

        try:
            data = self.conn.recv(self.BUFFER_SIZE)
            data = data.decode()
            data = str(data)
            logging.debug('DATA: ' + str(data))

            return data
        except socket.timeout:
            return None


    def send(self, ans):
        if self.conn is not None:
            ans = ans.encode()
            self.conn.sendall(ans)


    def close(self):
        self.s.close()
        if self.conn is not None:
            self.conn.close()
        self.conn = None
        logging.info("Connection has been closed.")
