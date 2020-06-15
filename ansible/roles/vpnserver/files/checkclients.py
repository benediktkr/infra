#!/usr/bin/env python3.8

# This is a really shitty script
# And i know it.

from socket import gethostname

from sudoisbot import sendmsg
from sudoisbot.common import getconfig, init

#config = getconfig()['checkclients']
config = init("checkclients")

#expected_clients = ["wifi001", "wifi002"]
expected_clients = config['expected_clients']
statefile = "/tmp/vpnclients.txt"

def notify(client_name, action):
    h = gethostname().split('.')[0]
    try:
        sendto = config['notify'][client_name]
        for a in sendto:
            sendmsg.send_msg(a, f"`{h}`: `{client}` has {action}")
    except KeyError:
        sendmsg.send_to_me(f"`{h}`: new client `{client}` has `{action}`")



if __name__ == "__main__":
    with open("/etc/openvpn/openvpn-status.log") as f:
        openvpnstatus = f.read()

    expt_connected = []
    for expt in expected_clients:
        if expt in openvpnstatus:
            expt_connected.append(expt)

    try:
        with open(statefile) as f:
            last = [a.strip() for a in f.readlines()]
    except IOError as e:
        if e.errno == 2:
            last = []
        else:
            raise

    s_last = set(last)
    s_conn = set(expt_connected)
    s_expt = set(expected_clients)

    if s_last != s_conn:
        missing = s_expt - s_conn
        new = s_conn - s_last

        if missing:
            # check if it was missing last time
            if s_last != s_conn:
                for client in missing:
                    notify(client, "disonnected")
        if new:
            for client in new:
                notify(client, "connected")
                #print "{} conected".format(client)

    with open(statefile, 'w') as f:
        f.write("\n".join(expt_connected))
