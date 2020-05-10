#!/usr/bin/env python3

import json

def get_state(statename="/tmp/temper_sub-state.json"):
    try:
        with open(statename, 'r') as f:
            return json.loads(f.read())
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return dict()

def update_state(update, statename, key=""):
    state = get_state(statename)
    try:
        name = update['name']
        state[update['name']] = update
    except TypeError:
        state[key] = update
    with open(statename, 'w') as f:
        f.write(json.dumps(state, indent=4))
