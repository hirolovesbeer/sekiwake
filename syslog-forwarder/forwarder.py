from socket import *

BUFSIZE = 65535
# BUFSIZE = 4096
DST_HOST = "172.16.0.12"
HOST = "0.0.0.0"
PORT = 514
DEBUG = 0

class SyslogForwarder():
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._count = 0
        self._sock = socket(AF_INET, SOCK_DGRAM)

#    def _forward(self, data):
#        if DEBUG:
#            print("Forwarding: '%s'" % (data))
#
#        #sock = socket(AF_INET, SOCK_DGRAM)
#        #sock.sendto(data, (DST_HOST, PORT))
#        self._sock.sendto(data, (DST_HOST, PORT))
#
#        # self._count = self._count + 1

    def listen(self):
        listensocket = socket(AF_INET, SOCK_DGRAM)
        listensocket.bind((self._host, self._port))

        while True:
            # addr = [ipaddr, port]
            # data, addr = listensocket.recvfrom(BUFSIZE)
#            data = listensocket.recv(BUFSIZE)
#            self._count = self._count + 1
#            # self._forward(data) # data and port
#            self._sock.sendto(data, (DST_HOST, PORT))

            # data = listensocket.recv(BUFSIZE)
            self._count = self._count + 1
            self._sock.sendto(listensocket.recv(BUFSIZE), (DST_HOST, PORT))

if __name__ == "__main__":
    try:
        server = SyslogForwarder(HOST, PORT)
        server.listen()
    except(IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print('count = ', server._count)
        print ("Crtl+C Pressed. Shutting down.")
