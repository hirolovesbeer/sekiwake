# Sekiwake
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
- syslog-forwarder.py
  - 0MQ subscriber
  - forward syslog to other server(s)
- xflow-forwarder.py
  - 0MQ Subscriber
  - forward xflow to other server(s)
- snmptrap-forwarder.py
  - 0MQ Subscriber
  - forward snmptrap to other server(s)
- send-syslog.py
  - test syslog sending program
- store-syslog.py
  - store syslog to disk
- anomaly-detection.py
  - syslog anomaly detection module using Bollinger Band algorithm
  - count total syslog message number in every minute(60 sec)
  - if count over 3 sigma(simple moving average + 3 x standard deviation), detect anomaly


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
                                  |     |     | <- capture.py
                                  | +-------+ |
                                  | | scapy | |
                                  | +-------+ |
                                  +-----------+
                                        |
                                    +-------+
                                    |libpcap|
                                    +-------+
                                        |
                            ------------------------ Network

```

# Environment
- macOS Sierra
- Ubuntu 16.10

# Dependency softwares
- This software made by python 3.5.2 using anaconda packages
- scapy-python3(pip install scapy-python3)
  - netifaces(pip install netifaces)
  - libpcap
    - macOS  : $ brew install libpcap
    - Ubuntu : $ sudo apt install libpcap-devel
  - libdnet
    - macOS
    ```
    $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null
    $ brew install autoconf automake
    $ brew link autoconf automake
    $ brew install libdnet
    ```
    - Ubuntu : $ sudo apt install libdnet-dev
- py3-netsyslog(pip install py3-netsyslog)
- 0MQ(ZeroMQ)
  - macOS
    - 0MQ, pyzmq
    ```
    $ brew install 0mq
    $ conda install pyzmq
    ```
  - Ubuntu : $ sudo apt-get install libzmq5-dev
- pandas, numpy
  - using anomaly detection module
    ```
    $ conda install numpy
    $ conda install pandas
    ```


# Performance measurement
- TBD
