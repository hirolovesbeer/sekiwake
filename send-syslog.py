import netsyslog
import syslog
import time
import argparse

HOST = '192.168.0.11'
COUNT = 1000
INTERVAL = 0.001

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        help='destination host',
                        type=str)
    parser.add_argument('--count',
                        help='send syslog count',
                        default=1000,type=int)
    parser.add_argument('--interval',
                        help='send syslog interval',
                        default=0.001,type=float)
    args = parser.parse_args()

    if args.host:
        HOST = args.host

    if args.count:
        COUNT = args.count

    if args.interval:
        INTERVAL = args.interval

    logger = netsyslog.Logger()
    logger.add_host(HOST)

    start = time.time()

    for i in range(0, COUNT):
        time.sleep(INTERVAL)
        msg = "Hey, it works " + str(i)
        logger.log(syslog.LOG_USER, syslog.LOG_NOTICE, msg, pid=True)

    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time)) + "[sec]"
