#! /usr/bin/env python

import sys
from scapy.all import sniff

import zmq
from zmq.utils.strtypes import asbytes

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:4999")

port='514'
host='192.168.0.1'

filter_rule = "udp and host {0} and port {1}".format(host, port)
#print(filter_rule)

packetCount = 0

def customAction(packet):
    global packetCount
    packetCount += 1

    print(packet.load)

    topic = b'syslog'
    message = asbytes(packet.load)
 
    # compose the message
    msg = "{0} ${1}".format(topic, message)
 
    print("Sending Message: {0}".format(msg))
 
    # send the message
    socket.send_multipart([topic, message])

    return "Packet #%s: %s ==> %s" % (packetCount, packet[0][1].src, packet[0][1].dst)    

sniff(iface="en0", prn=customAction, filter=filter_rule)
