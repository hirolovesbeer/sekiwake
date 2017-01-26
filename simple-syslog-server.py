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

#
# NO USER SERVICEABLE PARTS BELOW HERE...
#

import logging
import socketserver

logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')

class SyslogUDPHandler(socketserver.BaseRequestHandler):

    count = 0
    lines = []

    def handle(self):
        data = bytes.decode(self.request[0].strip())
        socket = self.request[1]
        #print( "%s : " % self.client_address[0], str(data))
        #logging.info(str(data))

        SyslogUDPHandler.lines.append(str(data))

        if SyslogUDPHandler.count == 1000:
            with open(LOG_FILE, mode='a') as fh:
                fh.write('\n'.join(SyslogUDPHandler.lines) + '\n')

            SyslogUDPHandler.count = 0
            SyslogUDPHandler.lines = []
            
#        with open(LOG_FILE, mode='a', encoding='utf-8') as fh:
#            fh.write(data + '\n')

        SyslogUDPHandler.count = SyslogUDPHandler.count + 1
#        print('count = ', SyslogUDPHandler.count)

if __name__ == "__main__":
    try:
        server = socketserver.UDPServer((HOST,PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=POLL_INTERVAL)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print('count = ', SyslogUDPHandler.count)
        print ("Crtl+C Pressed. Shutting down.")
