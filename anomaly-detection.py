import zmq
import threading

from collections import deque
import pandas as pd
import datetime

total_count = 0
window_size = 5
time_queue  = deque([], maxlen=window_size)
value_queue = deque([], maxlen=window_size)

def store_total_count():
    timer=threading.Timer(5, store_total_count)
    timer.start()

    global total_count
    print(total_count)

    now = datetime.datetime.now()

    append_time = now.strftime("%Y-%m-%d %H:%M:%S")
    time_queue.append(append_time)
    value_queue.append(total_count)

    calc_sigma(append_time)

    total_count = 0

def calc_sigma(time, sigma=3):
    print('hoge')
    data = pd.Series(value_queue, index=time_queue)
    print(data)

    # moving average
    # ma = data.rolling(center=False, window=window_size).mean()

    window_size = 1
    ma = data.rolling(center=False, window=window_size).mean()
    print(ma)

    window_size = 2
    std = data.rolling(center=False, window=window_size).std()
    print(std)

    std_plus = std.apply(lambda x: x * sigma)
    upper_limit = ma.add(std_plus)
    print(upper_limit)

    last_ul = std_plus.get(time)
    detect_anomaly(last_ul)

def detect_anomaly(upper_limit):
    if upper_limit > total_count:
        print("Find anomaly!!")
 
if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    socket.connect("tcp://127.0.0.1:4999")

    timer=threading.Thread(target=store_total_count)
    timer.start()

    while True:
        topic, msg = socket.recv_multipart()
        #print("{0}: {1}".format(topic, msg))

        if topic == b'syslog':
            #print("msg = %s" % msg)
            #store_total_count(count)
            total_count += 1
