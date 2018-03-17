import socket
import select
import json
import zlib

class Server():
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP sock

        self.server.setblocking(0)
        server_addr = ('localhost', 44139)

        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(server_addr)

        self.server.listen(128)
        self.server.settimeout(5)
        self.socks = [self.server]

        self.authorizations = {}

        while True:
            self.listen()

    def listen(self):
        r, w, e = select.select(self.socks, [], [], 0)

        for s in r:
            if s is self.server:
                sock, addr = s.accept()
                self.socks.append(sock)
                print('New connection from {}'.format(addr))

            else:
                try:
                    data = zlib.decompress(s.recv(4096)).decode()
                except ConnectionResetError:
                    print('Connection terminated')
                    self.kill(s)
                except zlib.error:
                    print('Connection terminated')
                    self.kill(s)

                else:
                    if data:
                        try:
                            request = json.loads(data)
                        except json.decoder.JSONDecodeError:
                            print('Connection sent bad data and has been terminated')
                            self.kill(s)

                        if s not in self.authorizations.keys():
                            if 'token' not in request.keys():
                                self.kill(s, 'UNAUTHORIZED')

                            self.authorization[s] = request['token']


        for s in e:
            print('Connection terminated')
            self.kill(s)

    def kill(socket, error=None):
        if error:
            socket.send(zlib.compress(json.dumps({'err' : error}).encode()))

        if socket in self.socks:
            self.socks.remove(socket)
        socket.close()
