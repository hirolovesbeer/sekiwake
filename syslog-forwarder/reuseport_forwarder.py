#!/usr/bin/env python

import sys, socket, time
from multiprocessing import Process

PORT = 514
NR_LISTENERS = 2

SO_REUSEPORT = 15

BUFSIZE = 1025
#DST_HOST = "10.206.116.22"
DST_HOST = "192.168.11.13"

def listener_work(num):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # set SO_REUSEADDR
    s.setsockopt(socket.SOL_SOCKET, SO_REUSEPORT, 1)   # set SO_REUSEPORT
    s.bind(("", PORT))

    while True:
        data, addr = s.recvfrom(BUFSIZE)
        s.sendto(data, (DST_HOST, PORT))

def server():
    processes = []
    for i in range(NR_LISTENERS):
        p = Process(target=listener_work, args=(i,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

def main():
    if '-s' in sys.argv:
        server()

if __name__ == '__main__':
    main()
