#!/usr/bin/env python3

from contextlib import contextmanager
from collections import namedtuple
from datetime import date
import stat
import os
import argparse
import sys
import subprocess
import getpass
import socket
import sys
import json
from shutil import which


class EsphArgumentParser():

    Arg = namedtuple('Arg', ['dest', 'args', 'kwargs'])

    def __init__(self, *args, **kwargs):
        # These are stored to amke _make_parser() simpler
        self._parser_args = args
        self._parser_kwargs = kwargs

        # Arguments are attached to _parser, and gets returend to the user if no subprarsers are created
        # If we dont have any subcommands/subparsers, we simply return _parser to the user without doing
        # anything special.
        self._parser = self._make_parser()

        # We also store arguments (attached to _parser) in _args. If we have subcommands/subparser, we read
        # tha arguments from _args, and attach them to all the subcommands, and then return _parser_subcmds
        # to the user.
        self._args = list()

        # subparsers get attached to _parser_subcmds. if subparsers are creater, we attach the arguments to
        # _parser_subcmds, and return that one to the user instead (_parser gets ignored)
        self._parser_subcmds = self._make_parser(exit_on_error=False)

        # If subparsers are created, we use  _subparsers (attached to _parser_subparsers) to hold them
        self._subparsers = None
        self._subparsers_dest = None

        # And we put all the subparsers in this dict, so we can attach arguments to them before returning
        # the parser to the user
        self._subcommands = dict()

    def _make_parser(self, exit_on_error=True):
        f=argparse.ArgumentDefaultsHelpFormatter
        return argparse.ArgumentParser(
            *self._parser_args,
            formatter_class=f,
            exit_on_error=exit_on_error,
            **self._parser_kwargs
        )

    @property
    def has_subcommands(self):
        return self._parser_subcmds._subparsers is not None

    def add_argument(self, *args, **kwargs):
        # Arguments get attached to _parser right away, that way we can get the 'dest' property that ArgumentParser
        # computes for us.
        arg = self._parser.add_argument(*args, **kwargs)

        # Then store the argument along with the 'dest' property as a NamedTuple in _args. If we have subcommands, we
        # will iterate over _args, and add the arguments to all the subparsers.
        #
        # The subparsers are attached to _parser_subcmds (via _subparsers).
        self._args.append(EsphArgumentParser.Arg(arg.dest, args, kwargs))

    def set_subcommand(self, dest, **kwargs):
        if self.has_subcommands:
            raise ValueError("cannot have multiple subcommands, use add_subcommand")

        # Now we have subcommands/subparsers. So we populate _subparsers (holds the group of sub parsers, attached
        # to _parser_subcmds)
        #
        # At this point we know that we wont be returning _parser to the user (but for simplicity we treat it the
        # same as before)
        #
        # Note that none of the subparsers (in _subparsers) have any arguments yet (so _parser_subcmds cant parse
        # any arguments current). It is only _parser that is aware of the arguments now.
        #
        # We have stored the arguments in _args as NamedTuple's. Before we return the parser to the user, we will
        # iterate over the list, and attach the arguments to all the subparsers.
        #
        # Since we now know we have subparsers/subcommands, _parser will not be returned to the user. We don't do
        # anything special with it thoug (to keep it simple), it just gets ignored (_parser_subcmds is returned insted).
        self._subparsers = self._parser_subcmds.add_subparsers(
            dest=dest,
            metavar=dest.upper(),
            required=True,
            **kwargs
        )
        self._subparsers_dest = dest

    def add_subcommand(self, command, *args, **kwargs):
        if not self.has_subcommands:
            raise ValueError("set subcommand with set_subcommand")

        # Each subparser/subcommand gets stored in the dict _subcommands, so that we can find them later and attach
        # all arguments from _args to all the subparsers. After that, we can return the _parser_subcmds parser to the
        # user.
        self._subcommands[command] = self._subparsers.add_parser(command, *args, **kwargs)

    def print_all_args(self):
        if self.has_subcommands:
            args = self._parser_subcmds.parse_args()
            value = getattr(args, self._subparsers_dest)
            print("[ ] Subcommand")
            print("dest".rjust(15), end=": ")
            print(self._subparsers_dest)
            print("value".rjust(15), end=": ")
            print(value)
        else:
            args = self._parser.parse_args()

        print("[ ] Arguments:")
        for item in self._args:
            dest = item.dest.rjust(20)
            value = getattr(args, item.dest)
            print(f"  {dest}".rjust(15), end=": ")
            print(value)
        raise SystemExit(0)

    def parse_args(self):
        # If we dont have any subparsers/subcommands, we just return the "regular" parser (that already has all
        # the arguments) to the user.
        if not self.has_subcommands:
            return self._parser.parse_args()

        # Otherwise, we add all the arguments to all the subparsers
        for subcmd in self._subcommands:
            for arg in self._args:
                self._subcommands[subcmd].add_argument(*arg.args, **arg.kwargs)

        # Workaround, the help output for _parser_subcmds doesnt include args when there is no subcmd (when
        # no subparser has matched)
        # Havent figured out a way to override the output, or insert the arguments to the root-level parser
        if len(sys.argv) <= 1 or sys.argv[1].startswith('-') or "-h" in sys.argv or "--help" in sys.argv:
            for arg in self._args:
                self._parser_subcmds.add_argument(*arg.args, **arg.kwargs)

        try:
            # Then return the _parser_subparser to the user instead.
            return self._parser_subcmds.parse_args()
        except argparse.ArgumentError:
            # Same workaround, but for usage output
            for arg in self._args:
                self._parser_subcmds.add_argument(*arg.args, **arg.kwargs)
            self._parser_subcmds.print_usage()
            raise SystemExit(1)


def get_domain():
    # this_hostname = socket.getaddrinfo(socket.gethostname(), 0, flags=socket.AI_CANONNAME)[0][3]
    this_hostname = socket.gethostname()
    parts = this_hostname.split('.')
    return ".".join(parts[1:])


def str_lower(value):
    return value.lower()

def get_parser():
    #parser = EsphArgumentParser(description="Wraps 'esphome', sets standard names via substitutions and aims to minimize number of YAML config files needed")
    parser = EsphArgumentParser()
    parser.set_subcommand('action', help="Command to pass to ESPHome.")

    parser.add_subcommand('clean', help="Delete all temporary build files and program binary.")
    parser.add_subcommand('config', help="Validate and print full YAML config.")
    parser.add_subcommand('compile', help="Read the config, validate it, compile a program and store a binary in target path.")
    parser.add_subcommand('upload', help="Validate the current config and upload the latest binary in target path.")
    parser.add_subcommand('logs', help="Connect to ESPHome device and print logs to stdout.")
    parser.add_subcommand('run', help="Validate, compile and upload the config.")
    parser.add_subcommand('version', help="Print ESPHome version to stdout.")
    parser.add_subcommand('esphome-help', help="Print ESPHome --help output.")
    parser.add_subcommand('substitutions', help="Show substitutions.")

    parser.add_argument("config", help="ESPHome config file.")

    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet output.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output.")
    parser.add_argument("-R", "--dry-run", action="store_true", help="Only log what would be run, without running it.")

    parser.add_argument("-l", "--show-log", action="store_true", help="Print logs from ESPHome device to stdout.")
    parser.add_argument("-u", "--user", action="store_true", help=f"Run as '{getpass.getuser()}', otherwise sudo's to 'hass'.")
    parser.add_argument("-s", "--substitution", nargs=2, action="append", metavar=("key", "value"), help="ESPHome substitutions")
    parser.add_argument("-d", "--domain", default=get_domain(), type=str_lower, help="Domain for hostname.")
    parser.add_argument("-n", "--name", help="Device name. Hostname becomes 'esphome-${name}'")
    parser.add_argument("-D", "--device", help="Device name to upload program to. Can be device file (example: /dev/ttyUSB0) or hostname (can be used when renaming device).")
    parser.add_argument("-N", "--no-device", action="store_true", help="Ignore found device files and computed hostnames, and do not attempt to write to them.")


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


def make_subs(names, args_subs, config, domain):

    build_target = get_esphome_path(getpass.getuser(), "target")
    subs = {
        **names,
        "room_name": names['room_name'],
        "lower_node_name": names["lower_node_name"],
        "lower_underscored_node_name": names["lower_underscored_node_name"],
        "friendly_node_name": f'{names["friendly_node_name"]}',
        "domain": f".{domain}",
        "device_type_name": names["device_type_name"],
        "hostname": names["hostname"],
        "config_name": os.path.basename(os.path.basename(config)),
        "config_date": date.today().isoformat(),
        # this is the hostname, without the esphome- prefix
        "build_path": f"{build_target}/{names['dashed_node_name']}"
    }
    if args_subs is not None:
        for key, val in args_subs:
            subs[key] = val

    return subs

def make_esphome_cmd(args, names, subs, esphome_user, usb_dev):
    print(f"esphome user: '{esphome_user}'")
    esphome_virtualenv_path = get_esphome_virtualenv_path(esphome_user)
    print(f"virtualenv: '{esphome_virtualenv_path}'")
    esphome_exec = which_esphome(esphome_virtualenv_path)

    if args.action == "help":
        return ["-h"]

    esphome_dir = get_esphome_path(esphome_user)
    #build_target = get_esphome_path(esphome_user, "target")
    # esphome_packages = get_esphome_path(esphome_user, "packages")
    # esphome_secrets = get_esphome_path(esphome_user, ".secrets")

    print(f"esphome dir: '{esphome_dir}'")
    print(f"esphome exec: '{esphome_exec}'")
    print(json.dumps(subs, indent=2))

    esphome_cmd = [esphome_exec]
    if args.quiet:
        esphome_cmd.append("-q")
    if args.verbose:
        esphome_cmd.append("-v")

    if args.config.count('/') == 0:
        config = f"{esphome_dir}/devices/{args.config}"
    else:
        config = f"{esphome_dir}/{args.config}"


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

    if args.action == "test":
        parser.print_all_args()
        raise SystemExit(0)

    usb_dev = get_usb_device()
    if usb_dev is not None:
        print(f"USB device: '{usb_dev}'")

    if args.user:
        esphome_user = getpass.getuser()
    else:
        esphome_user = "hass"

    names = make_names(args.config, args.name, args.domain)
    subs = make_subs(names, args.substitution, args.config, args.domain)
    if args.action == "substitutions":
        print(json.dumps(subs, indent=2))
        raise SystemExit(0)

    print(f"friendly_node_name: '{names['friendly_node_name']}'")
    print(f"hostname: '{names['hostname']}'")
    print(f"domain: '{args.domain}'")
    print(f"fqdn: '{names['fqdn']}'")
    print()

    with run_with_cpugov("performance"):
        esphome_cmd = make_esphome_cmd(args, names, subs, esphome_user, usb_dev)
        subps(esphome_cmd, username=esphome_user, dry_run=args.dry_run)

    print()
    print(f"fqdn: '{names['fqdn']}'")


if __name__ == "__main__":
    os.environ["TERM"] = "xterm256-color"
    main()
