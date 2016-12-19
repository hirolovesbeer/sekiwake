import zmq
 
if __name__ == "__main__":
    dst = '192.168.0.2'

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    socket.connect("tcp://127.0.0.1:4999")
 
    while True:
        topic, msg = socket.recv_multipart()
        print("{0}: {1}".format(topic, msg))

        if topic == b'xflow':
            print("dst = %s" % dst)
