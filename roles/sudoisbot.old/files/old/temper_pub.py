#!/usr/bin/python3 -u

import json
import time
from datetime import datetime
import os

import zmq

from temper import Temper

# temper = Temper()
# t = temper.read()
# temp = t[0]['internal temperature']

def publisher(name, addr, sleep_time):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    # to limit number of messages held in memory:
    # ZMQ_HWM - high water mark. default: no limit
    # http://api.zeromq.org/2-1:zmq-setsockopt

    # And even though I'm the publisher, I can do the connecting rather
    # than the binding
    #socket.connect('tcp://127.0.0.1:5000')
    socket.connect(addr)
    print(f"Connected to {addr}")

    while True:
        temper = Temper()
        t = temper.read()
        try:
            data = {
                'name': name,
                'temp': t[0]['internal temperature'],
                'timestamp': datetime.now().isoformat()
            }
            sdata = json.dumps(data)
            #print(sdata)
            socket.send_string(f"temp: {sdata}")
        except KeyError:
            print(repr(t))

        time.sleep(sleep_time)

    socket.close()

if __name__ == "__main__":

    try:
        name = os.environ["TEMPER_PUB_NAME"]
        addr = os.environ["TEMPER_PUB_ADDR"]
        sleep_time = os.environ["TEMPER_PUB_SLEEP"]
    except KeyError as e:
        print(f"Missing environment variable '{e}'")

    publisher(name, addr, int(sleep_time))
