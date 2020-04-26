#!/usr/bin/env python3
import argparse
import json

import zmq

# So that you can copy-and-paste this into an interactive session, I'm
# using threading, but obviously that's not what you'd use

def sink():
    marker = b"temp: "
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, marker)
    # Even though I'm the subscriber, I'm allowed to get this party
    # started with `bind`
    socket.bind('tcp://127.0.0.1:5000')

    cutoff = len("temp: ")
    while True:
        bytedata = socket.recv()
        bytejson = bytedata[cutoff:]
        j = json.loads(bytejson)
        print(j)


if __name__ == "__main__":
    sink()
