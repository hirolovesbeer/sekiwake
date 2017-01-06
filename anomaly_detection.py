''' This program is anomaly detection module for sekiwale framework '''

import threading

from collections import deque
import datetime
import warnings
warnings.filterwarnings('ignore')
import pandas as pd

import zmq

TIMER_SEC = 5
TOTAL_COUNT = 0
WINDOW_SIZE = 5
MIN_PERIODS = 2
TIME_QUEUE = deque([], maxlen=WINDOW_SIZE)
VALUE_QUEUE = deque([], maxlen=WINDOW_SIZE)


def store_total_count():
    '''
    count store method to queues
    '''

    timer = threading.Timer(TIMER_SEC, store_total_count)
    timer.start()

    global TOTAL_COUNT
    print(TOTAL_COUNT)

    now = datetime.datetime.now()

    append_time = now.strftime("%Y-%m-%d %H:%M:%S")
    TIME_QUEUE.append(append_time)
    VALUE_QUEUE.append(TOTAL_COUNT)

    calc_sigma(append_time)

    TOTAL_COUNT = 0


def calc_sigma(time, sigma=3):
    '''
    calculation Bollinger Band algorithm
    '''

    print('hoge')
    data = pd.Series(VALUE_QUEUE, index=TIME_QUEUE)
    print(data)

    moving_average = data.rolling(center=False, window=WINDOW_SIZE,
                                  min_periods=MIN_PERIODS).mean()
    print(moving_average)

    std = data.rolling(center=False, window=WINDOW_SIZE,
                       min_periods=MIN_PERIODS).std()
    print(std)

    std_plus = std.apply(lambda x: x * sigma)
    upper_limit = moving_average.add(std_plus)
    print(upper_limit)

    last_ul = std_plus.get(time)
    detect_anomaly(last_ul)


def detect_anomaly(upper_limit):
    '''
    detect anomaly method
    '''

    if TOTAL_COUNT > upper_limit:
        print("Find anomaly!!")


if __name__ == "__main__":
    ZMQ_CONTEXT = zmq.Context()
    ZMQ_SOCKET = ZMQ_CONTEXT.socket(zmq.SUB)
    ZMQ_SOCKET.setsockopt_string(zmq.SUBSCRIBE, '')
    ZMQ_SOCKET.connect("tcp://127.0.0.1:4999")

    COUNT_THREAD = threading.Thread(target=store_total_count)
    COUNT_THREAD.start()

    while True:
        TOPIC, MSG = ZMQ_SOCKET.recv_multipart()
        # print("{0}: {1}".format(TOPIC, MSG))

        if TOPIC == b'syslog':
            # print("MSG = %s" % MSG)
            # store_total_count(count)
            TOTAL_COUNT += 1
