#!/usr/bin/env python3

# ohttps://ubntwiki.com/products/software/unifi-controller/api

import urllib3
urllib3.disable_warnings()
import json

import requests

# dont check this in...
people_json = "/usr/local/etc/people.json"

def get_session(controller, username, password):
    s = requests.Session()
    login = s.post(f"{controller}/api/login",
                   json={
                       'username': username,
                       'password': password},
                   verify=False)
    login.raise_for_status()
    return s

def get_clients(session, controller):
    # should just stuff the controller url in the session object
    clients = session.get(f"{controller}/api/s/default/stat/sta")
    clients.raise_for_status()
    return clients.json()['data']

def get_client_names(session, controller):
    names = list()
    try:
        for client in get_clients(session, controller):
            try:
                name = client.get('hostname', client['ip'])
                names.append(name)
            except KeyError:
                # device has neither ip nor hostname
                # something fucky is happening
                print(f"weird client on unifi: {client}")
        return names
    except requests.exceptions.ConnectionError:
        raise

def people_home(session, controller):
    home = set()
    try:
        with open(people_json, 'r') as f:
            people = json.loads(f.read())
    except FileNotFoundError:
        people = dict()
        #raise

    names = get_client_names(session, controller)
    for name in names:
        if name in people:
            home.add(people[name])
    return home


if __name__ == "__main__":
    import sys
    controller = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    print(f"controller: {controller}")
    session = get_session(controller, username, password)
    print("connected:")
    for name in get_client_names(session, controller):
        print(f"* {name}")
    print("home:")
    for name in people_home(session, controller):
        print(f"* {name}")
