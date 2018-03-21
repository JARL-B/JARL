import socket
import select
import json
import zlib
import sys
import requests

class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(2)

        try:
            request = requests.get('https://gist.github.com/JellyWX/fe22b9e726f22de8e03f8d5b4b044013/raw')
            connection_info = json.loads(request.text)
        except:
            print('backup connection mode')
            connection_info = {"ip" : "54.37.19.136", "port" : 44139}

        try:
            self.client.connect((connection_info['ip'], connection_info['port']))
        except:
            sys.exit()

        try:
            with open('token', 'r') as f:
                self.token = f.read().strip()
        except FileNotFoundError:
            self.token = input('Please enter your token now > ')

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
                print('Error: Server reports ' + data['err'])

            print('incoming > ' + str(data))

        f = open('input', 'r')
        for line in f:
            if line:
                self.client.send(zlib.compress(line.encode()))
                open('input', 'w').close()
        f.close()

c = Client()

while True:
    c.get_response()
