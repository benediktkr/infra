#!/usr/bin/env python3

from contextlib import contextmanager
from datetime import date
import stat
import os
import argparse
import sys
import subprocess
import getpass
import socket
import json
from shutil import which


def get_domain():
    # this_hostname = socket.getaddrinfo(socket.gethostname(), 0, flags=socket.AI_CANONNAME)[0][3]
    this_hostname = socket.gethostname()
    parts = this_hostname.split('.')
    return ".".join(parts[1:])


def str_lower(value):
    return value.lower()


def get_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("action")
    parser.add_argument("config")
    parser.add_argument("-d", "--device")
    parser.add_argument("--no-device", action="store_true")
    parser.add_argument("--domain", default=get_domain(), type=str_lower)
    parser.add_argument("-n", "--name")
    parser.add_argument("-s", "--substitution", nargs=2, action="append", metavar=("key", "value"),)
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--show-log", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--user", action="store_true")
    parser.add_argument("--room")
    return parser


def is_dev(device_path):
    try:
        return stat.S_ISCHR(os.stat(device_path).st_mode)
    except FileNotFoundError:
        return False


# def check_is_devs(*args):
#     return {
#         a: is_dev(f"/dev/{a}")
#         for a in args }
#
# def get_usb_device2():
#     devices = check_is_dev(
#         "tty.usbmodem01",
#         "ttyUSB0",
#         "ttyUSB1",
#         "ttyACM0",
#         "ttyACM1",
#         "ttyACM2"
#    )

def get_usb_device():
    usbmodem01 = "/dev/tty.usbmodem01"
    usb0 = "/dev/ttyUSB0"
    usb1 = "/dev/ttyUSB1"
    acm0 = "/dev/ttyACM0"
    acm1 = "/dev/ttyACM1"
    acm2 = "/dev/ttyACM2"

    if is_dev(usbmodem01):
        return usbmodem01

    elif is_dev(usb0):
        return usb0
    elif is_dev(usb1):
        return usb1

    elif is_dev(acm0) and is_dev(acm1) and is_dev(acm2):
        return acm2
    elif is_dev(acm0) and not (is_dev(acm1) or is_dev(acm2)):
        return acm0
    else:
        return None


def get_esphome_path(username, esphome_subdir=""):
    esphome = os.path.expanduser(f"~{username}/esphome")
    if esphome_subdir == "":
        return esphome
    else:
        return f"{esphome}/{esphome_subdir}"


def get_esphome_virtualenv_path(username):
    virtualenv = ".cache/virtualenvs/esphome"
    homedir = os.path.expanduser(f"~{username}")
    return f"{homedir}/{virtualenv}"


def which_esphome(esphome_virtualenv_path):
    esphome_virtualenv_bin = f"{esphome_virtualenv_path}/bin/esphome"

    if os.path.exists(esphome_virtualenv_bin):
        return esphome_virtualenv_bin
    else:
        for item in ["esphome.py", "esphome"]:
            if which(item) is not None:
                return which(item)
        else:
            print(f"ERROR path does not exist: '{esphome_virtualenv_bin}")
            sys.exit(1)


def subps(command, username=None, show_output=True, dry_run=False):
    if not isinstance(command, list):
        command = command.split(" ")

    if username is not None and username != getpass.getuser():
        sudo = ["sudo"]
        if username != "root":
            #sudo.extend(["-u", username])
            sudo = []
    else:
        sudo = []

    cmd = sudo + command

    print(f"+ {' '.join(cmd)}")
    try:
        if not dry_run:
            ps = subprocess.run(cmd, capture_output=not show_output, cwd="/tmp")
            return ps.returncode
        else:
            return 0
    except subprocess.CalledProcessError as e:
        if not show_output:
            print("stdout:")
            print(e.stdout)
            print("--")
            print("stderr:")
            print(e.stderr)
        sys.exit(e.returncode)


def get_cpu_govenor():
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def set_cpu_govenor(govenor):
    current = get_cpu_govenor()
    if current is not None:
        if govenor != current:
            cmd = ["cpupower", "frequency-set", "-g", govenor]
            subps(cmd, show_output=False, username="root")
            print(f"changed cpu_govenor to: '{govenor}'\n")


@contextmanager
def run_with_cpugov(set_cpugov):
    current_cpugov = get_cpu_govenor()
    if current_cpugov is None:
        has_cpugov = False
    else:
        has_cpugov = True

    try:
        if has_cpugov:
            set_cpu_govenor(set_cpugov)
        else:
            print("no cpu govenor")
        yield
    except KeyboardInterrupt:
        print()
        print("Aborting")
        print()
        sys.exit(13)
    finally:
        if has_cpugov:
            print()
            set_cpu_govenor(current_cpugov)


def make_esphome_cmd(args, names, esphome_user, usb_dev):
    print(f"esphome user: '{esphome_user}'")
    esphome_virtualenv_path = get_esphome_virtualenv_path(esphome_user)
    print(f"virtualenv: '{esphome_virtualenv_path}'")
    esphome_exec = which_esphome(esphome_virtualenv_path)

    if args.action == "help":
        return ["-h"]

    esphome_dir = get_esphome_path(esphome_user)
    #build_target = get_esphome_path(esphome_user, "target")
    build_target = get_esphome_path(getpass.getuser(), "target")
    print(f"esphome dir: '{esphome_dir}'")
    print(f"esphome exec: '{esphome_exec}'")
    print(f"esphome build_target: '{build_target}'")

    esphome_cmd = [esphome_exec]
    if args.quiet:
        esphome_cmd.append("-q")
    if args.verbose:
        esphome_cmd.append("-v")

    if args.config.count('/') == 0:
        config = f"{esphome_dir}/devices/{args.config}"
    else:
        config = f"{esphome_dir}/{args.config}"

    # esphome_packages = get_esphome_path(esphome_user, "packages")
    # esphome_secrets = get_esphome_path(esphome_user, ".secrets")

    subs = {
        **names,
        "room_name": names['room_name'],
        "lower_node_name": names["lower_node_name"],
        "lower_underscored_node_name": names["lower_underscored_node_name"],
        "friendly_node_name": f'{names["friendly_node_name"]}',
        "domain": f".{args.domain}",
        "device_type_name": names["device_type_name"],
        "hostname": names["hostname"],
        "config_name": os.path.basename(os.path.basename(config)),
        "config_date": date.today().isoformat(),
        # this is the hostname, without the esphome- prefix
        "build_path": f"{build_target}/{names['dashed_node_name']}"
    }
    print(json.dumps(subs, indent=2))

    for item in [("-s", k, v) for k, v in subs.items()]:
        esphome_cmd.extend(item)

    esphome_cmd.extend([
        args.action,
        config,
        # esphome_packages,
        # esphome_secrets
    ])

    if args.action in ["run", "upload", "logs"]:

        if usb_dev is not None:
            prompt = input(f"USB device detected on '{usb_dev}', continue? ")
            if prompt.lower() not in ["yes", "y"]:
                raise SystemExit("User aborted.")
            else:
                esphome_cmd.extend(["--device", usb_dev])
        elif not args.no_device:
            esphome_cmd.extend(["--device", names["fqdn"]])

    if args.action == "run" and not args.show_log:
        esphome_cmd.append("--no-logs")

    print(f"\nesphome cmd: '{' '.join(esphome_cmd)}'\n")
    return esphome_cmd


def make_names(config_filename, name, domain):
    config_filename = os.path.basename(config_filename)
    device_type_name = config_filename.split('.yaml')[0].replace("_", "-")
    if name is None:
        node_name = device_type_name
    else:
        node_name = name

    node_name_lower = node_name.lower()
    node_name_lower_underscored = node_name_lower.replace(" ", "_").replace("-", "_")
    node_name_dashed = node_name_lower.replace(" ", "-").replace("_", "-")
    hostname = f"esphome-{node_name_dashed}"
    if len(hostname) > 31:
        raise SystemExit(f"hostname is too long (max 31 characters): {hostname}")

    parts = node_name.replace("-", " ").replace("_", " ").split(" ", 1)
    if len(parts) > 1:
        head, tail = parts
        friendly_node_name = " ".join([head.title()] + [a if a.isupper() else a.lower() for a in tail.split(" ")])
        if any(head.lower().endswith(a) for a in ["room", "way", "tchen"]):
            room_name = head.title()
        else:
            room_name = "WHATSAROOM"
    else:
        friendly_node_name = node_name.title()
        room_name = "NOROOM"

    return {
        'node_name': node_name,
        'lower_node_name': node_name_lower,
        'lower_underscored_node_name': node_name_lower_underscored,
        'dashed_node_name': node_name_dashed,
        'friendly_node_name': friendly_node_name,
        'hostname': hostname,
        'room_name': room_name,
        'device_type_name': device_type_name,
        'fqdn': f"{hostname}.{domain}"
    }


def main():
    parser = get_parser()
    args = parser.parse_args()

    usb_dev = get_usb_device()
    if usb_dev is not None:
        print(f"USB device: '{usb_dev}'")

    if args.user:
        esphome_user = getpass.getuser()
    else:
        esphome_user = "hass"

    names = make_names(args.config, args.name, args.domain)
    print(f"friendly_node_name: '{names['friendly_node_name']}'")
    print(f"hostname: '{names['hostname']}'")
    print(f"domain: '{args.domain}'")
    print(f"fqdn: '{names['fqdn']}'")
    print()

    with run_with_cpugov("performance"):
        esphome_cmd = make_esphome_cmd(args, names, esphome_user, usb_dev)
        subps(esphome_cmd, username=esphome_user, dry_run=args.dry_run)

    print()
    print(f"fqdn: '{names['fqdn']}'")


if __name__ == "__main__":
    os.environ["TERM"] = "xterm256-color"
    main()
