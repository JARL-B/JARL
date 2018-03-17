import socket
import select
import json
import zlib
import sys

class Client():
    def __init__(self, screen):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(2)

        try:
            self.client.connect(('localhost', 44139))
        except:
            sys.exit()

    def get_response(self):
        r, w, e = select.select([self.client], [], [], 0)

        if self.client in r:
            data = zlib.decompress(self.client.recv(4096)).decode()
            if not data:
                print('Connection terminated')
                sys.exit()

            print(data)

        f = open('input', 'r')
        for line in f:
            if line.endswith('\n')
