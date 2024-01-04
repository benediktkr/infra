#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os


# https://ken.cheo.dev/notes/ansible/installing-ansible-2.12-with-all-dependencies-with-pipx/

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('playbook')
    parser.add_argument('--diff', action="store_true")
    parser.add_argument('--inventory', default='hosts.yml')
    #parser.add_argument('--check', action="store_true")
    #parser.add_argument('--limit')
    #parser.add_argument('--extra-vars')
    return parser


def get_args():
    parser = get_parser()
    args, ansible_args =  parser.parse_known_args()
    return args, ansible_args

def get_path_repo():
    path_self = os.path.realpath(__file__)
    path_bin = os.path.dirname(path_self)
    path_repo = os.path.dirname(path_bin)
    return path_repo

def ansible_playbook_full_path(playbook):
    path_repo = get_path_repo()
    return os.path.join(path_repo, "private", "playbooks", playbook)

def ansible_playbook():
    args, ansible_args = get_args()

    #if 'ANSIBLE_INVENTORY' not in os.environ:
    #    path_repo = get_path_repo()
    #    os.environ["ANSIBLE_INVENTORY"] = os.path.join(path_repo, "private", "hosts.yml")
    path_repo = get_path_repo()
    #os.environ['ANSIBLE_PLAYBOOK_VARS_ROOT'] = os.path.join(path_repo, "private")
    os.environ['ANSIBLE_PLAYBOOK_VARS_ROOT'] = "all"
    os.environ['ANSIBLE_INVENTORY'] = os.path.join(path_repo, "private", "playbooks", args.inventory)

    path_playbook = ansible_playbook_full_path(args.playbook)
    cmd = [
        "ansible-playbook",
        path_playbook,
        *ansible_args
    ]

    print(f"[>] cmd: '{' '.join(cmd)}'")
    try:
        ps = subprocess.run(cmd, check=True)
        rc = ps.returncode
        print(f"[ ] exited with: '{rc}'")
        sys.exit(rc)
    except FileNotFoundError:
        print(f"[!] ansible-playbook is not installed or in PATH")
        print(f"    install with 'pipx':")
        print(f"      pipx install --include-deps ansible")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        rc = e.returncode
        print(f"[!] exited with error: '{rc}'")
        sys.exit(rc)


if __name__ == "__main__":
    ansible_playbook()

