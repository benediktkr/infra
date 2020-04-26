#!/usr/bin/env python3

import argparse
import json
import time
from datetime import datetime

import zmq

from temper import Temper

# temper = Temper()
# t = temper.read()
# temp = t[0]['internal temperature']

def publisher(name):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    # And even though I'm the publisher, I can do the connecting rather
    # than the binding
    socket.connect('tcp://127.0.0.1:5000')


    while True:
        temper = Temper()
        t = temper.read()
        temp = t[0]['internal temperature']
        now = datetime.now().isoformat()
        data = {'name': name, 'temp': temp, 'timestamp': now}
        sdata = json.dumps(data)
        print(sdata)
        socket.send_string(f"temp: {sdata}")
        time.sleep(60)

    socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    publisher(args.name)
