import socket
import select
import json
import zlib
import sys

class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(2)

        try:
            self.client.connect(('localhost', 44139))
        except:
            sys.exit()

        self.token = input('Please enter your token now > ')
        self.authorized = False

        self.client.send(zlib.compress(json.dumps({'token' : self.token}).encode()))

    def get_response(self):
        r, w, e = select.select([self.client], [], [], 0)

        if self.client in r:
            try:
                data = zlib.decompress(self.client.recv(4096)).decode()
            except zlib.error:
                print('Connection terminated')
                sys.exit()

            if not data:
                print('Connection terminated')
                sys.exit()

            data = json.loads(data)
            if 'err' in data.keys():
                print('Server reports ' + data['err'] + '. Connection has been closed.')

            print(data)

        f = open('input', 'r')
        for line in f:
            if line:
                self.client.send(zlib.compress(line.encode()))
                open('input', 'w').close()
        f.close()

c = Client()

while True:
    c.get_response()
