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
    clients = session.get(f"{controller}/api/s/default/stat/sta")
    clients.raise_for_status()
    return clients.json()['data']


def people_home(session, controller):
    try:
        with open(people_json, 'r') as f:
            people = json.loads(f.read())
    except FileNotFoundError:
        people = dict()
        #raise

    try:
        home = set()
        for client in get_clients(session, controller):
            hostname = client['hostname']
            if hostname in people:
                home.add(people[hostname])

        return home
    except requests.exceptions.ConnectionError:
        raise

if __name__ == "__main__":
    import sys
    controller = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    print(f"controller: {controller}")
    session = get_session(controller, username, password)
    for client in get_clients(session, controller):
        print(f"* {client['hostname']}")
