#!/usr/bin/python3 -u
import os
import json

import zmq

from simplestate import update_state

def append_txt(update, csvdir):
    # could split into files per day/week/month/year
    #if fname.endswith(".txt"):
    #    fname = fname[:-4] + f".{update['name']}.json"
    #else:
    #    fname = fname + ".json"
    fname = csvdir + f"/temper_sub.{update['name']}.csv"
    # write csv to save some space
    short_timestamp = update['timestamp'][:19] # no millisec
    s = f"{short_timestamp},{update['temp']}"
    with open(fname, 'a') as f:
        f.write(s + "\n")

def sink(addr, csvdir, state):
    timeout = 1000*60*5
    marker = b"temp: "
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, marker)
    socket.setsockopt(zmq.RCVTIMEO, timeout)
    # Even though I'm the subscriber, I'm allowed to get this party
    # started with `bind`
    #socket.bind('tcp://*:5000')

    socket.connect(addr)
    print(f"Connected to: '{addr}'")

    cutoff = len("temp: ")
    while True:
        try:
            bytedata = socket.recv()
        except zmq.error.Again:
            secs = timeout // 1000
            print(f"timed out after {secs} seconds")
            print(f"Reconnecting to {addr}")
            socket.connect(addr)

        bytejson = bytedata[cutoff:]
        j = json.loads(bytejson)
        if state:
            update_state(j, state)
        if csvdir:
            append_txt(j, csvdir)

        # import random
        # if random.randint(0, 10) == 10:
        #     print(j)


if __name__ == "__main__":

    state = os.environ.get("TEMPER_SUB_STATE", "")
    csvdir = os.environ.get("TEMPER_SUB_CSVDIR", "")
    addr = os.environ["TEMPER_SUB_ADDR"]

    if state:
        print(f"Maintaining state file: '{state}'")
    if csvdir:
        print(f"Saving csvfiles to: '{csvdir}'")

    sink(addr, csvdir, state)
