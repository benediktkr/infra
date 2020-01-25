#!/usr/bin/env python2.7

# This is a really shitty script
# And i know it.
# It runs python2.7 because theres a bug with sudoisbot in python3
# its not meant to be a great script
# might get around to fixing it at some point
# or not

from sudoisbot import sendmsg

expected_clients = ["wifi001", "wifi002"]
statefile = "/tmp/vpnclients.txt"

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
                    sendmsg.send_to_me("{} has disconnected".format(client))
        if new:
            for client in new:
                sendmsg.send_to_me("{} has connected".format(client))
                #print "{} conected".format(client)

    with open(statefile, 'w') as f:
        f.write("\n".join(expt_connected))
