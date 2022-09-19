#!/bin/env python3

import sys
import json

CONFIG = '/usr/local/etc/restic-passwords.json'


def read_password(repo_name):
    with open(CONFIG, 'r') as f:
        j = json.load(f)

    return j[repo_name]['password']


def get_password(repo_name):
    try:
        return read_password(repo_name)
    except KeyError:
        raise SystemExit(f"no password found for '{repo_name}' in '{CONFIG}'")


def main():
    try:
        repo_name = sys.argv[1]
    except IndexError:
        raise SystemExit(f"usage {sys.argv[0]} <repo_name>")

    password = get_password(repo_name)
    print(password)
    sys.exit(0)


if __name__ == "__main__":
    main()
