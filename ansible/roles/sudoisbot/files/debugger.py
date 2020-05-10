#!/usr/bin/python3 -u

import argparse
import zmq


def sub(addr):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    socket.connect(addr)

    print("Subscribed to {}".format(addr))

    while True:
        bytedata = socket.recv()
        print(repr(bytedata))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--addr", default="tcp://192.168.1.2:5560")
    args = parser.parse_args()

    sub(args.addr)
