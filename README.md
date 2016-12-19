# sekiwake
This software is prototype of syslog/xflow/snmptrap forwarder.

# Concept
- Capture syslog/xflow/snmptrap packet directly using libpcap
- Using pub/sub model
  - Publish packet capture data to 0MQ(ZeroMQ)
  - Subscriber get data from 0MQ and processing(forward syslog/xflow/snmptrap)
- 0MQ pub/sub model
  - Aim to scale out forwarder

# Programs
- capture.py
  - packet capture program using scapy(libpcap)
  - 0MQ publisher
- forwarder.py
  - 0MQ subscriber
  - forward syslog to other server(s)
- send-syslog.py
  - test syslog sending program

# System image
```
  +-------+                      +-------------+
  |  dst  |                      |   notify    |
  | server|                      |             |
  +-------+                      +-------------+
      ^                                 ^
      |                                 |
+-----------+                    +-------------+                   +-------------+
| +-------+ |                    | +---------+ |                   | +---------+ |
| | s/x/t-| |                    | | anomaly | |                   | |  other  | |
| |forward| |                    | |detection| |                   | |functions| |
| +-------+ |                    | +---------+ |                   | +---------+ |
|     |     | <- syslog/xflow/   |      |      | <- anomaly-       |      |      |
| +-------+ |    trap-           | +---------+ |    detection.py   | +---------+ |
| |  sub  | |    forwarder.py    | |   sub   | |                   | |   sub   | |
| |  0MQ  | |                    | |   0MQ   | |                   | |   0MQ   | |
| +-------+ |                    | +---------+ |                   | +---------+ |
+-----------+                    +-------------+                   +-------------+
      ^                                 ^                                 ^
      |                                 |                                 |
      +---------------------------------+---------------------------------+
      |
      |       <- 0MQ(pub/sub model)
      |
+-----------+
| +-------+ |
| |  pub  | |
| |  0MQ  | |
| +-------+ |
|     |     | <- cap-syslog.py
| +-------+ |
| | scapy | |
| +-------+ |
+-----------+
      |
  +-------+
  |libpcap|
  +-------+
      |
  --------- Network

```

# Dependency softwares
- This software made by python 3.5.2 using anaconda packages
- scapy-python3(pip install scapy-python3)
  - netifaces(pip install netifaces)
  - libpcap(brew install libpcap)
  - libdnet

    ```
    $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null
    $ brew link autoconf automake
    $ brew install libdnet
    ```
- py3-netsyslog(pip install py3-netsyslog)
- 0MQ(ZeroMQ)


# Performance measurement
- TBD
