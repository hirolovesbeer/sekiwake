#!/usr/bin/env python

## Tiny Syslog Server in Python.
##
## This is a tiny syslog server that is able to receive UDP based syslog
## entries on a specified port and save them to a file.
## That's it... it does nothing else...
## There are a few configuration parameters.

LOG_FILE = '/var/tmp/test.log'
HOST, PORT = "0.0.0.0", 514
POLL_INTERVAL = 0.001

DST_HOST = '172.16.0.10'

#
# NO USER SERVICEABLE PARTS BELOW HERE...
#

import netsyslog
import syslog

import logging
import socketserver

logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')

class SyslogUDPHandler(socketserver.BaseRequestHandler):

    count = 0
    nslogger = netsyslog.Logger()
    nslogger.add_host(DST_HOST)

    def handle(self):
        data = bytes.decode(self.request[0].strip())
        #socket = self.request[1]
        #print( "%s : " % self.client_address[0], str(data))
        #logging.info(str(data))

        SyslogUDPHandler.nslogger.log(syslog.LOG_USER, syslog.LOG_INFO, str(data), pid=False)

        SyslogUDPHandler.count = SyslogUDPHandler.count + 1


if __name__ == "__main__":
    try:
        server = socketserver.UDPServer((HOST,PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=POLL_INTERVAL)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print('count = ', SyslogUDPHandler.count)
        print ("Crtl+C Pressed. Shutting down.")
