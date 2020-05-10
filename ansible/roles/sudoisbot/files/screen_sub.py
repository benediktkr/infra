#!/usr/bin/python3 -u

# written for py3.5 because thats what was on the zero

# sudo cp screen_sub.py /usr/local/sbin
# sudo mv screen_sub.systemd /etc/systemd/system/screen_sub.service
# sudo systemctl --system daemon-reload
# sudo systemctl enable screen_sub
# sudo systemctl start screen_sub

import argparse
from datetime import datetime, timedelta
import json

import dateutil.parser
import zmq

try:
    from PIL import ImageFont
    import inkyphat
    have_inky = True
except ImportError:
    have_inky = False


def log(text):
    if have_inky:
        # assuming systemd and syslog
        print(text)
    else:
        ts = datetime.now().isoformat()[:19]
        s = "{}\t{}".format(ts, text)
        print(s)
        with open("/tmp/screen_sub.log", 'a') as f:
            f.write(s + "\n")

def should_update(last_updated, min_update_interval, debug=False):
    if last_updated == False:
        if debug:
           log("last_updated is False")
        return True
    # TBB: discard flood messages

    now = datetime.now()
    age = now - last_updated
    next_ = min_update_interval - age.seconds

    if debug:
        if next_ > 0:
            log("next update in {} seconds".format(next_))
        else:
            log("pub forcing, last update was: {} sec ago".format(abs(next_)))

    if next_ <= 0:
        return True
    else:
        #log("next update in {} seconds".format(next))
        return False


def gettext(message):
    MAX_LINES = 8
    text = message['text']
    have = len(text.strip().split('\n'))
    fillers = '\n'*(max(MAX_LINES - have, 0))
    timestamp = message['timestamp'].replace("T", " ")[:16]
    updated = timestamp
    # doesnt handle too long messagse fix later
    return text.strip() + fillers + updated

def sub(addr, debug):
    timeout = 1000*60*5
    marker = b"eink: "
    cutoff = len(marker)
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, marker)
    socket.setsockopt(zmq.RCVTIMEO, timeout)

    socket.connect(addr)
    last_updated = False # wrong type :)

    log("Subscribed to {}".format(addr))
    log("Subscription: {}".format(marker))

    while True:
        # wait for updates
        try:
            bytedata = socket.recv()
        except zmq.error.Again:
            secs = timeout // 1000
            log("timed out after {} seconds".format(secs))
            log("Reconnecting to {}".format(addr))
            socket.connect(addr)

        bytejson = bytedata[cutoff:]
        j = json.loads(bytejson.decode("utf-8"))

        # shortening mui means what the loop decides to using
        # for minimum_update_interval
        default_mui = 2*60
        mui = int(j.get('min_update_interval', default_mui))

        if debug:
            log("received: " + repr(bytejson.decode("utf-8")))
            log("mui: {}".format(mui))

        if should_update(last_updated, mui, debug):
            if not have_inky:
                log("would update e-ink display")
            text = gettext(j)
            if have_inky:
                inkyphat.set_colour("red")
                inkyphat.set_rotation(j.get("rotation", 0))
                font = inkyphat.ImageFont.truetype(
                    inkyphat.fonts.PressStart2P, 8)
                xy = (10, 10)
                fill = inkyphat.BLACK
                inkyphat.clear()
                inkyphat.text(xy, text, fill=fill, font=font)
                inkyphat.show()
                if mui == 0:
                    log("e-ink screen updated (forced)")
                else:
                    log("e-ink screen updated")
            last_updated = datetime.now()

        else:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--addr", default="tcp://192.168.1.2:5560")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    log("Have inky: {}".format(have_inky))
    sub(args.addr, args.debug)
