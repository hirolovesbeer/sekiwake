import netsyslog
import syslog
import time

logger = netsyslog.Logger()
logger.add_host("192.168.0.1")

for i in range(0, 3):
    time.sleep(0.1)
    msg = "Hey, it works " + str(i)
    logger.log(syslog.LOG_USER, syslog.LOG_NOTICE, msg, pid=True)
