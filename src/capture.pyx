''' This program is capture packet using libpcap and send captured packet to 0MQ publisher '''

#! /usr/bin/env python

import argparse

from scapy.all import sniff
import msgpack

import zmq
from zmq.utils.strtypes import asbytes

CONTEXT = zmq.Context()
SOCKET = CONTEXT.socket(zmq.PUB)
SOCKET.bind("tcp://127.0.0.1:4999")

DEBUG = True
MSGPACK = False

# capture src addr(host)
HOST = '192.168.0.11'
INTERFACE = 'enp0s8'

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

    if DEBUG:
        print(packet.load)

    topic = b''
    if str(packet[0][1].dport) == SYSLOG_PORT:
        topic = b'syslog'
        message = asbytes(packet.load)

        # compose the message
        msg = "{0} ${1}".format(topic, message)

        if DEBUG:
            print("Sending Message: {0}".format(msg))

        # send the message
        # test binary send
        # import zlib
        # message = zlib.compress(message)
        if MSGPACK:
            msg = msgpack.packb([topic, message])
            SOCKET.send(msg)
        else:
            SOCKET.send_multipart([topic, message])
    elif str(packet[0][1].dport) == NETFLOW_PORT:
        topic = b'xflow'
    elif str(packet[0][1].dport) == SFLOW_PORT:
        topic = b'xflow'
    elif str(packet[0][1].dport) == SNMPTRAP_PORT:
        topic = b'snmptrap'
    else:
        print('other something')

    if DEBUG:
        "Packet #%s: %s ==> %s" % (PACKET_COUNT, packet[0][1].src, packet[0][1].dst)

    return

#if __name__ == "__main__":
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--iface',
                        help='select capture interface',
                        type=str)
    parser.add_argument('--debug',
                        default=False, action='store_true')
    parser.add_argument('--msgpack',
                        default=False, action='store_true')
    args = parser.parse_args() 

    if args.iface:
        print("capture interface is ", args.iface)
        INTERFACE = args.iface

    if args.debug:
        print("debug mode")
        DEBUG = True

    if args.msgpack:
        print("use msgpack")
        MSGPACK = True

    try:
        filter_rule = "udp and host {0} and (port {1} or port {2} or port {3} or port {4})".format('192.168.0.11', '514', '2055', '6343', '162')
        sniff(iface='enp0s8', prn=custom_action, filter=filter_rule)
        #sniff(iface=INTERFACE, prn=custom_action, filter=FILTER_RULE)
    except OSError:
        print("No such device: ", args.iface)
