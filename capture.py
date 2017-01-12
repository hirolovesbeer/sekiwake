''' This program is capture packet using libpcap and send captured packet to 0MQ publisher '''

#! /usr/bin/env python

from scapy.all import sniff

import zmq
from zmq.utils.strtypes import asbytes

CONTEXT = zmq.Context()
SOCKET = CONTEXT.socket(zmq.PUB)
SOCKET.bind("tcp://127.0.0.1:4999")

# capture src addr(host)
HOST = '192.168.0.1'
INTERFACE = 'en1'

SYSLOG_PORT = '514'
NETFLOW_PORT = '2055'
SFLOW_PORT = '6343'
SNMPTRAP_PORT = '162'

FILTER_RULE = "udp and host {0} and (port {1} or port {2} or port {3} or port {4})".format(HOST, SYSLOG_PORT, NETFLOW_PORT, SFLOW_PORT, SNMPTRAP_PORT)
# print(FILTER_RULE)

PACKET_COUNT = 0


def custom_action(packet):
    '''
    module for zero mq publish
    '''

    global PACKET_COUNT
    PACKET_COUNT += 1

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
        # import zlib
        # message = zlib.compress(message)
        SOCKET.send_multipart([topic, message])
    elif str(packet[0][1].dport) == NETFLOW_PORT:
        topic = b'xflow'
    elif str(packet[0][1].dport) == SFLOW_PORT:
        topic = b'xflow'
    elif str(packet[0][1].dport) == SNMPTRAP_PORT:
        topic = b'snmptrap'
    else:
        print('other something')

    return "Packet #%s: %s ==> %s" % (PACKET_COUNT, packet[0][1].src, packet[0][1].dst)

sniff(iface=INTERFACE, prn=custom_action, filter=FILTER_RULE)
