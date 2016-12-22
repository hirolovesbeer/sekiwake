import zmq

test_path = '/var/tmp/test.log'

def store_log(path, msg):
    with open(path, mode='a', encoding='utf-8') as fh:
        fh.write(msg.decode('utf-8') + '\n')
 
if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    socket.connect("tcp://127.0.0.1:4999")
 
    while True:
        topic, msg = socket.recv_multipart()
        print("{0}: {1}".format(topic, msg))

        if topic == b'syslog':
            #print("msg = %s" % msg)
            store_log(test_path, msg)
