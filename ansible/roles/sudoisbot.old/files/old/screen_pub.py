#!/usr/bin/python3 -u

# ansible for now

import argparse
import json
import time
from datetime import datetime, timedelta
import os

import dateutil.parser
import zmq
import requests.exceptions

from simplestate import get_state
import unifi

def bark():
    import random
    numberofwoofs = random.randint(1,3)
    woofs = "woof " * numberofwoofs
    return woofs.strip()

def temps():
    state = get_state()
    t = list()
    for k, v in state.items():
        # check for old temps and dont send those
        delta = datetime.now() - timedelta(minutes=10)
        if dateutil.parser.parse(v['timestamp']) > delta:
            temp = v['temp']
            t.append(f"{k}: {temp} C")
    return '\n'.join(t)

def people_home():

    controller = os.environ["UNIFI_CONTROLLER"]
    username = os.environ["UNIFI_USERNAME"]
    password = os.environ["UNIFI_PASSWORD"]

    try:
        session = unifi.get_session(controller, username, password)
        home = unifi.people_home(session, controller)
    except requests.exceptions.ConnectionError:
        return "home: (connection error)"
    if home:
        return "home: " + ', '.join(home)
    else:
        return "nobody home"

def publisher(name, loop, sleep_time, woof, rotation, update_interval=None):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    # just hold the last message in memory
    # screen doesnt care about missed updates
    #socket.setsockopt(zmq.ZMQ_HWM, 1)
    addr = "tcp://192.168.1.2:5559"
    print(f"Connected to {addr}")
    socket.connect(addr)

    # will force an update on first loop
    last_home = ""
    while True:
        home_update = False
        if woof:
            text = bark()
        else:
            currently_home = people_home()
            # has anyone come or gone?
            if len(currently_home) != len(last_home):
                home_update = True
            rona = "wash hands and shoes off"
            text = temps() + '\n' + currently_home  + '\n\n' + rona
            last_home = currently_home


        now = datetime.now().isoformat()
        # force more frequent updates for debugging
        #  'min_update_interval': 60
        data = {
            'name': name,
            'text': text,
            'timestamp': now,
            'rotation': 0
        }
        # if nobody is at home then lets just update every 3 hours
        if last_home == "nobody home":
            data['min_update_interval'] = 60*60*3
        # but force screen update if "people home" changes
        if home_update:
            data['min_update_interval'] = 0
        # otherwise override with --update-interval
        elif update_interval is not None:
            data['min_update_interval'] = update_interval

        sdata = json.dumps(data)
        socket.send_string(f"eink: {sdata}")
        # if home_update:
        #     # notify telegram?
        #     print(f"eink: {sdata}")

        if not loop:
            break
        else:
            time.sleep(sleep_time)

    socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="cron")
    parser.add_argument("--one-off", action="store_true")
    parser.add_argument("--woof", action="store_true")
    parser.add_argument("--sleep-time", default=60, type=int)
    parser.add_argument("--rotation", type=int)
    parser.add_argument("--update-interval", type=int, default=15*60)

    args = parser.parse_args()

    loop = not args.one_off

    publisher(args.name, loop, args.sleep_time, args.woof, args.rotation, args.update_interval)
