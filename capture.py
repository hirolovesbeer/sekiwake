#! /usr/bin/env python

import sys
from scapy.all import sniff

import zmq
from zmq.utils.strtypes import asbytes

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:4999")

# capture src addr(host)
HOST = '192.168.0.1'

INTERFACE = 'en1'
SYSLOG_PORT = '514'
NETFLOW_PORT = '2055'
SFLOW_PORT = '6343'
SNMPTRAP_PORT = '162'

filter_rule = "udp and host {0} and (port {1} or port {2} or port {3} or port {4})".format(HOST, SYSLOG_PORT, NETFLOW_PORT, SFLOW_PORT, SNMPTRAP_PORT)
#print(filter_rule)

packetCount = 0

def customAction(packet):
    global packetCount
    packetCount += 1

    print(packet.load)

    topic = b''
    if str(packet[0][1].dport) == SYSLOG_PORT:
        topic = b'syslog'
        message = asbytes(packet.load)
 
        # compose the message
        msg = "{0} ${1}".format(topic, message)
 
        print("Sending Message: {0}".format(msg))
 
        # send the message
        # test binary send
        #import zlib
        #message = zlib.compress(message)
        socket.send_multipart([topic, message])
    elif str(packet[0][1].dport) == NETFLOW_PORT:
        topic = b'xflow'
    elif str(packet[0][1].dport) == SFLOW_PORT:
        topic = b'xflow'
    elif str(packet[0][1].dport) == SNMPTRAP_PORT:
        topic = b'snmptrap'
    else:
        print('other something')

    return "Packet #%s: %s ==> %s" % (packetCount, packet[0][1].src, packet[0][1].dst)    

sniff(iface=INTERFACE, prn=customAction, filter=filter_rule)
