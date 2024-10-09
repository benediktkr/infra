#!/bin/env python3

import sys
import os
import argparse
import subprocess
import shutil

from loguru import logger

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init-user", help="create new home dir base for a given user")

    return parser.parse_args()

def list_users(homepath="/home"):
    ignore = [".system"]
    users = [u for u in os.listdir(homepath) if u not in ignore]
    return users

def copy_dir(src, dest):
    p = subprocess.call(["cp", "-ra", src, dest])
    return p

def get_paths(user):
    home_base = os.path.join("/usr/local/homes", user)
    home = os.path.join("/home", user)

    return (home_base, home)

def init_ephemeral_home(user):
    """does the INVERSE of reset_home_dir

    meant to be run when a user is created. might be a better way
    """
    home_base, home = get_paths(user)
    if os.path.exists(home_base):
        shutil.rmtree(home_base)

    copy_dir(home, home_base)
    logger.info(f"created {home_base}'")

def reset_home_dir(user):
    home_base, home = get_paths(user)
    if not os.path.exists(home_base):
        init_ephemeral_home(user)

    shutil.rmtree(home)
    copy_dir(home_base, home)
    logger.debug(f"reset {home}")

def main():

    logger.remove()
    logger.add(sys.stderr, level="INFO")

    args = parse_args()

    if args.init_user:
        logger.info(f"creating new base dir for '{args.init_user}'")
        init_ephemeral_home(args.init_user)
    else:
        for user in list_users():
            reset_home_dir(user)


if __name__ == "__main__":
    main()
