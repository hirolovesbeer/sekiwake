import socket

class sender():

    PORT = 514

    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._hostnames = {}

    def add_host(self, hostname):
        self._hostnames[hostname] = 1

    def remove_host(self, hostname):
        del self.hostnames[hostname]

    def send(self, packet):
        fro hostname in self._hostnames:
            self._sock.sendto(str(packet), (hostname, self.PORT))
