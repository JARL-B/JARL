import socket
import select
import json

class Server():
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP sock

        self.server.setblocking(0)
        server_addr('localhost', 44139)

        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(server_addr)

        self.server.listen(128)
        self.server.settimeout(5)
        self.socks = [self.server]

    def listen(self):
        r, w, e = select.select(self.socks, [], [], 0)

        for s in r:
            if s is self.server:
                sock, addr = s.accept()
                self.socks.append(sock)
                print('New connection from {}'.format(addr))

            else:
                try:
                    data = s.recv(4096).decode()
                except ConnectionResetError:
                    print('Connection terminated')
                    if s in self.socks:
                        self.socks.remove(s)
                    s.close()

                if data:
                    try:
                        request = json.loads(data)
                    except json.decoder.JSONDecodeError:
                        print('Connection sent bad data and has been terminated')
                        if s in self.socks:
                            self.socks.remove(s)
                        s.close()

                    if request['']


        for s in e:
            print('Connection terminated')
            if s in self.socks:
                self.socks.remove(s)
            s.close()
