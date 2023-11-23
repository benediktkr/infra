#!/usr/bin/env python3

import argparse
import os

import yaml


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--read-path", help="path to known_devices.yaml file to clean up", default="/var/lib/hass/home-assistant/config/known_devices.yaml")
    parser.add_argument("-w", "--write-path", help="path to write cleaned known_devices.yaml file to")
    return parser


def read_known_devices(kd_path):
    try:
        with open(kd_path, "r") as f:
            return yaml.safe_load(f)
    except yaml.scanner.ScannerError:
        raise SystemExit(f"invalid yaml: '{kd_path}'")
    except FileNotFoundError:
        raise SystemExit(f"file not found: '{kd_path}'")


def write_cleaned_known_devices(ckd_path, cleaned_known_devices):
    with open(ckd_path, "w") as f:
        yaml.dump(cleaned_known_devices, f)


def is_mac_item(entity_id, device):
    """Used to identify entries like:

    5b_0f_df_82_de_94:
      name: 5B:0F:DF:82:DE:94
      mac: BLE_5B:0F:DF:82:DE:94
      icon:
      picture:
      track: true


    the yaml dict key is the mac address, using '_', as a delimter,
    and the 'name' key has the mac address, in upper case, using the
    usual ':' delimeter for mac addresses.

    the 'mac' key has the mac address prefixed with 'BLE_'.

    entity_id: the yaml-dict key
    friendly_name: the 'name' key of the yaml-dict
    """
    return is_mac(entity_id, delimiter="_") or is_mac(device['name'])


def is_mac(s, delimiter=":"):
    parts = s.split(delimiter)
    return len(parts) == 6 and all(is_hex(a) for a in parts)


def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def iter_clean_known_devices(known_devices):
    for entity_id, device in known_devices.items():
        if not is_mac_item(entity_id, device):
            yield entity_id, device


def clean_known_devices(known_devices):
    return dict(iter_clean_known_devices(known_devices))


def rename_known_device(entity_id, device):
    tracker_types = ["BLE", "BT"]
    friendly_name = device['name']
    try:
        tracker_type, mac = device['mac'].split("_", 1)
    except ValueError:
        pass

    if tracker_type in tracker_types and is_mac(mac):
        prefix = tracker_type.lower()
        entity_id_parts = entity_id.split("_")
        friendly_name_parts = friendly_name.split(" ")

        if entity_id_parts[0].lower() != prefix:
            new_entity_id = f"{prefix}_{entity_id}"

        tracker_type_friendly_alts = [tracker_type, f"({tracker_type})", f"[{tracker_type}]"]
        if not any(a.upper() in tracker_type_friendly_alts for a in friendly_name_parts):
            new_friendly_name = f"{friendly_name} ({tracker_type})"



def main():
    parser = make_parser()
    args = parser.parse_args()

    known_devices = read_known_devices(args.read_path)
    print(f"known_devices.yaml: {len(known_devices)} devices")

    cleaned_known_devices = clean_known_devices(known_devices)
    print(f"cleaned known_devices.yaml: {len(cleaned_known_devices)} devices")
    print(f"removed from known_devices.yaml: {len(known_devices) - len(cleaned_known_devices)} devices")

    if args.write_path is not None:
        write_cleaned_known_devices(args.write_path, cleaned_known_devices)
        print(f"wrote cleaned known_devices.yaml to '{args.write_path}'")

    #diff = set(known_devices) - set(cleaned_known_devices)
    #for item in diff:
    #    import json
    #    print(json.dumps({item: known_devices[item]}, indent=2))


if __name__ == "__main__":
    main()
