import argparse
import zmq
import msgpack

test_path = '/var/tmp/test.log'

DEBUG = False
MSGPACK = False

def store_log(path, msg):
    with open(path, mode='a', encoding='utf-8') as fh:
        fh.write(msg.decode('utf-8') + '\n')
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug',
                        default=False, action='store_true')
    parser.add_argument('--msgpack',
                        default=False, action='store_true')
    args = parser.parse_args()

    if args.debug:
        print("debug mode")
        DEBUG = True

    if args.msgpack:
        print("use msgpack")
        MSGPACK = True


    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    socket.connect("tcp://127.0.0.1:4999")
 
    while True:

        if MSGPACK:
            message = socket.recv()
            topic, msg = msgpack.unpackb(message)
        else:
            topic, msg = socket.recv_multipart()

        if DEBUG:
            print("{0}: {1}".format(topic, msg))

        if topic == b'syslog':
            if DEBUG:
                print("msg = %s" % msg)
            store_log(test_path, msg)
