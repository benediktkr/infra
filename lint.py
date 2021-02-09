#!/usr/bin/python3

from os import walk, path
import yaml
import argparse
import sys


# doesnt work
# just use yamllint: https://github.com/adrienverge/yamllint

def main():
    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    return lint()

def is_yaml(fname):
    return path.splitext(fname)[1] in [".yml", ".yaml"]

def valid_yaml(yaml_file):
    try:
        with open(yaml_file, 'r') as f:
            yaml.safe_load(f)
        return True
    except FileNotFoundError:
        print(f"file not found: '{yaml_file}'")
        return False

def lint():
    invalid = list()
    for dirpath, dirnames, filenames in walk("."):
        yaml_files = [f for f in filenames if is_yaml(f)]
        for fname in yaml_files:
            full_path = path.join(dirpath, fname)
            if not valid_yaml(full_path):
                print(f"invalid yaml: '{full_path}'")
                invalid.append(full_path)
    return len(invalid)

if __name__ == "__main__":
    sys.exit(main())
