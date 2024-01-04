#!/usr/bin/env python3

import argparse
import json
from json.decoder import JSONDecodeError


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--indent", type=int)
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


def fix_json(json_path, json_indent):
    try:
        with open(json_path) as f:
            json_file_contents = f.read()

        json_data = json.loads(json_file_contents)
        json_string = json.dumps(json_data, indent=json_indent)

        if json_string != json_file_contents:
            with open(json_path, 'w') as f:
                f.write(json_string + "\n")
            return True
        else:
            return False
    except (PermissionError, FileNotFoundError, JSONDecodeError) as e:
        print(type(e).__name__, end=": ")
        print(e)
        raise SystemExit("aborting.") from e


def main():
    args = parse_args()
    json_file_changed = fix_json(args.path, args.indent)

    if json_file_changed and not args.quiet:
        print(f"fixed: {args.path}")


if __name__ == "__main__":
    main()
