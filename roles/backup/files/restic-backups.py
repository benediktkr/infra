#!/bin/env python3

import argparse
import sys
import os
import json
import subprocess

from loguru import logger


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repo', default='main')

    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('--config', default='/usr/local/etc/restic.json')
    parser.add_argument('--log-level', default='INFO')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--no-excludes', action='store_true')
    parser.add_argument('--log-file',
                        default='/var/log/backup/restic-backups.log')

    args, restic_args = parser.parse_known_args()
    return (args, restic_args)


def setup_logging(repo_name, log_file, args_log_level, quiet):
    log_level = os.environ.get("SUDOIS_LOG_LEVEL", args_log_level.upper())
    log_format = " ".join([
        "<green><dim>{time:YYYY-MM-DDT}</dim>{time:HH:mm:ss}<dim>{time:Z}</dim></green>", # noqa
        "<dim><yellow>repo={extra[repo]}</yellow></dim>",
        "<dim><level>{level: >8}</level></dim>",
        "<level>{message}</level>"
    ])
    handlers = [{
            'sink': sys.stderr,
            'format': log_format,
            'level': "ERROR" if quiet else log_level
        },
        {
            'sink': log_file,
            'format': log_format,
            'level': log_level,
            'rotation': "4 weeks",
            'retention': "1 year",
            'serialize': True
        }
    ]
    logger.configure(handlers=handlers, extra={'repo': repo_name})


def read_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)


def restic_password_command(repo_name):
    return f"/usr/local/bin/restic-password.py {repo_name}"


def prepare_env(repo_name, repo_config):
    restic_env = dict()

    passwd_cmd = restic_password_command(repo_name)
    restic_env.update({'RESTIC_PASSWORD_COMMAND': passwd_cmd})

    if 'env' in repo_config:
        restic_env.update(repo_config['env'])

    logger.debug(f"setting env vars: {' '.join(restic_env.keys())}")

    # its also possible to pass subprocess.run(env=dict()) but then
    # we dont get the parent process' env with us
    os.environ.update(restic_env)


def list_sshfs_mounts():
    cmd = "findmnt -t fuse.sshfs --json".split(' ')
    ps = subprocess.run(cmd, capture_output=True)
    if ps.stdout == b'':
        return []
    else:
        mounts = json.loads(ps.stdout)
        return [a['target'] for a in mounts['filesystems']]


def run_restic(repo_url, restic_args, no_excludes, dry_run):
    restic_cmd = ["restic", "-r", repo_url]
    restic_cmd.extend(restic_args)

    if "backup" in restic_args and not no_excludes:
        restic_cmd.extend([
            "--exclude-file", "/usr/local/etc/backup-excludes.txt"
        ])

    for item in list_sshfs_mounts():
        restic_cmd.extend([
            "--exclude", item
        ])

    logger.debug(" ".join(restic_cmd))
    if dry_run:
        logger.warning("this was a dry run, no changes have been made")
        return

    # .run(env={}) is possible (but then child doesnt inherit parent env)
    return subprocess.run(restic_cmd, check=True)

def find_nobackup(config):
    # very interesting restic option:
    #
    # restic backup --help
    # [...]
    #
    # --exclude-if-present filename[:header]   takes filename[:header], exclude
    #       contents of directories containing filename (except filename itself)
    #       if header of that file is as provided (can be specified multiple times)
    #
    pass

def main():
    args, restic_args = parse_args()
    setup_logging(args.repo, args.log_file, args.log_level, args.quiet)
    config = read_config(args.config)

    # sets the RESTIC_PASSWORD_COMMAND and other env vars as needed
    repo_config = config[args.repo]
    prepare_env(args.repo, repo_config)
    return run_restic(
        repo_config['url'], restic_args, args.no_excludes, args.dry_run)


if __name__ == "__main__":
    main()
