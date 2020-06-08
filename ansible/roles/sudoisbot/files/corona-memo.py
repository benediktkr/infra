#!/usr/bin/env python3

"""Remind me to wash hands and take shoes off"""

import time

import sudoisbot

from simplestate import get_state, update_state
import unifi

statename = "/tmp/corona.json"

while True:
    state = get_state(statename).get('home', set())
    home = unifi.people_home()
    just_arrived = home - set(state)
    if 'B' in just_arrived:
        print("wash hands and shoes off")

    update_state(list(home), statename, 'home')

    if "B" in state or "B" in just_arrived:
        print(f"Sleeping 2 because im home {state}")
        time.sleep(2.0)

    else:
        print(f"Sleeping 3 because im not home {state}")
        time.sleep(3) # 30*60
