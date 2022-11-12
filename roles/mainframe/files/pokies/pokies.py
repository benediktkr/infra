#!/bin/env python3

# mainframe ~/infra/roles/mainframe/files <main*> $ sudo -u ansible python3 -m pip install --user paramiko

import json
from base64 import b64decode
from argparse import ArgumentParser

import paramiko.client
from loguru import logger


class SSHClient(paramiko.client.SSHClient):
    def iter_cmd(self, cmd, timeout=None):
        if isinstance(cmd, list):
            command = " ".join(cmd)
        else:
            command = cmd

        stdin, stdout, stderr = self.exec_command(command, timeout=timeout)
        return stdout.readlines()

    def cmd(self, command):
        lines = self.iter_cmd(command)
        return "\n".join(lines)



def get_file_b64:
    with open(file_path, 'r') as f:
        return  b64encode(f.read())


def print_cmd(self, iter_output):
    for line in iter_output:
        print(line)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("destination", help="which pokies to rub")
    parser.add_argument("-u", "--user", help="ssh user")
    parser.add_argument("-i", "--identity-file", help="ssh key")
    parser.add_argument("--rub", help="what to rub on the other end",
                        required=True)
    parser.add_argument("--path", help="for --rub upload")
    return parser.parse_args()

def main():
    args = parse_args()

    logger.info(f"pokies: {args.destination}")
    logger.info(f"rubbing: {args.rub}")

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(
        args.destination,
        username=args.user,
        key_filename=args.identity_file,
        look_for_keys=False,
        allow_agent=False
    )

    if args.rub == "upload":
        pass
    if args.rub == "touch":
        j = json.dumps({'rub': args.rub, "path": args.path})
        rub_out = ssh.cmd(j)
    else:
        rub_out = ssh.cmd(args.rub)

    print(rub_out)

if __name__ == "__main__":
    main()
