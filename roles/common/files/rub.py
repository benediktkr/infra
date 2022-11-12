#!/usr/bin/python3 -u

# unbuffered

import sys
import os
import subprocess
import getpass
import json

"""
command="/usr/local/bin/rub.py"
"""


# idea: read stdin, pokies.py writes to its stdout
# read from rub.py's stdin. lineinput or something?

def subps_run(cmd):
    try:
        p = subprocess.run(
            cmd.split(' '),
            capture_output=True,
            check=False
        )
        if p.stdout:
            print(p.stdout)
        if p.stderr:
            print(p.stderr)

        p.check_returncode()
        return p

    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"error: {e}")
        sys.exit(1)


def nginx():
    cmds = [
        "nginx -t",
        "systemctl reload nginx"
    ]
    for cmd in cmds:
        subps_run(cmd)


def wg0():
    p = subps_run("sudo systemctl reload wg-quick@wg0")
    print("reloaded: wg-quick@wg0")


def main():
    ssh_original_cmd = os.environ.get('SSH_ORIGINAL_COMMAND', None)
    print(f"SSH_ORIGINAL_COMMAND={ssh_original_cmd}")

    j = json.loads(ssh_original_cmd)
    rub = j['rub']

    print(f"getting rubbed: '{rub}'")

    if rub == "ruok":
        print('iamok')
    elif rub == "nginx":
        nginx()
    elif rub == "wg0":
        wg0()
    else:
        print(f"unkonwn: '{rub}'")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
