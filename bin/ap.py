#!/usr/bin/env python3

## Got used to this at Care.com

import os
import sys
import subprocess
import yaml

def get_secrets_file(secretsfile):
    with open('private/inventory.d/' + secretsfile, 'r') as f:
        secrets = yaml.load(f)
    return secrets

if __name__ == '__main__':
    envs = get_secrets_file("ap.yml")['envs']
    for name, value in envs.items():
        os.environ[name] = value


    args = ["ansible"] + sys.argv[1:]
    print("Executing", " ".join(args))
    subprocess.call(args)
