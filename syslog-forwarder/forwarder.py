from socket import *

BUFSIZE = 65535
#BUFSIZE = 1024
DST_HOST = "10.6.6.22"
#DST_HOST2 = "10.6.6.23"
HOST = "0.0.0.0"
PORT = 514
DEBUG = 0

LOG_PATH = '/var/tmp/test.log'

class SyslogForwarder():
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._count = 0
        self._sock = socket(AF_INET, SOCK_DGRAM)
        self._logpath = LOG_PATH

    def store_log(self, msg):
        with open(self._logpath, mode='a', encoding='utf-8') as fh:
            fh.write(msg.decode('utf-8'))

    def listen(self):
        listensocket = socket(AF_INET, SOCK_DGRAM)
        listensocket.bind((self._host, self._port))

        while True:
            # comment: addr = [ipaddr, port]
            data, addr = listensocket.recvfrom(BUFSIZE)
            self._sock.sendto(data, (DST_HOST, PORT))
#            self._sock.sendto(data, (DST_HOST2, PORT))

            self._count = self._count + 1
#            self.store_log(data)
#            self._sock.sendto(listensocket.recvfrom(BUFSIZE)[0], (DST_HOST, PORT))


if __name__ == "__main__":
    try:
        server = SyslogForwarder(HOST, PORT)
        server.listen()
    except(IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print('count = ', server._count)
        print ("Crtl+C Pressed. Shutting down.")
