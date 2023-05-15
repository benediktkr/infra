#!/usr/bin/env python3

import argparse
from datetime import datetime
import subprocess
import json
import sys
import shutil
import os
import time

from loguru import logger
import dateutil.parser
from dateutil.parser._parser import ParserError

def delete_file(file_path):
    try:
        os.remove(file_path)
        logger.debug(f"deleted: '{file_path}'")
    except FileNotFoundError:
        pass


def replace_file(src, dest):
    try:
        logger.debug(f"src: {src}, dest: {dest}")
        delete_file(dest)
        shutil.move(src, dest)
        logger.debug(f"replaced '{dest}'")
    except (PermissionError, OSError, FileNotFoundError) as e:
        logger.error(e)
        raise SystemExit(2)


def ffprobe_get_tags(file_path):
    cmd = [
        "ffprobe",
        "-v", "quiet",
        file_path,
        "-print_format", "json",
        "-show_entries",
        "stream_tags:format_tags"
    ]
    try:
        p = subprocess.run(cmd, capture_output=True, check=True)
        j = json.loads(p.stdout)
        return j['format']['tags']
    except subprocess.CalledProcessError as e:
        logger.error(f"{cmd[0]} exited with returncode {e.returncode} \n{e.stderr.decode()}")
        raise SystemExit(e.returncode)
    except KeyError as e:
        logger.error(f"key {e} for file '{file_path}' not found in ffprobe stdout: {p.stdout.decode()}")
        raise SystemExit(2)


def ffmpeg_write_date_tag(podcast_file, out_file, iso_date_str):
    delete_file(out_file)

    cmd = [
        "ffmpeg",
        "-nostdin",
        "-y",   # overwrite output file
        "-i", podcast_file,
        #"-c",  "copy",
        "-metadata",  f"date={iso_date_str}",
        #"-metadata", f"releasedate={iso_date_str}",
        out_file
    ]

    try:
        p = subprocess.run(cmd, capture_output=True, check=True, stdin=None)
        p.check_returncode()
        logger.debug(f"output: '{out_file}'")
        replace_file(out_file, podcast_file)
    except subprocess.CalledProcessError as e:
        logger.error(f"{cmd[0]} exited with returncode {e.returncode} \n{e.stderr.decode()}")
        raise SystemExit(e.returncode)
    finally:
        delete_file(out_file)


def eyeD3_write_date_tag(podcast_file, iso_date_str):

    # import eyeD3 ?

    podcast_dir = os.path.basename(podcast_file)
    cover_path = os.path.join(podcast_dir, "cover.jpg")

    cmd = [
        "eyeD3",
        "--release-date", iso_date_str,
        "--orig-release-date", iso_date_str,
        "--recording-date", iso_date_str,
        # this overwrites 'release date' i think:
        #"--release-year", iso_date_str.split("-")[0],
        #"--preserve-file-times"
    ]
    # if os.path.exists(cover_path):
    #     cmd.extend(["--add-image", f"{cover_path}:FRONT_COVER"])
    cmd.append(podcast_file)

    logger.debug(" ".join(cmd))

    try:
        subprocess.run(cmd, capture_output=True, check=True, stdin=None)
        logger.debug(f"updated: '{podcast_file}'")
    except subprocess.CalledProcessError as e:
        logger.error(f"{cmd[0]} exited with returncode {e.returncode} \n{e.stderr.decode()}")
        raise SystemExit(e.returncode)


def get_podcast_name_from_dir(podcast_file):
    podcast_dir = os.path.dirname(podcast_file)
    if podcast_dir.startswith("/"):
        # for now lets just do absolute dirs for names
        podcast_name = os.path.basename(podcast_dir)
        logger.debug(f"podcast name: {podcast_name}")
        return podcast_name
    else:
        return None


def eyeD3_write_album_tag(podcast_file, podcast_name):
    # "album" is the name of the podcast

    cmd = ["eyeD3", "--album", podcast_name, podcast_file]
    try:
        subprocess.run(cmd, capture_output=True, check=True, stdin=None)
    except subprocess.CalledProcessError as e:
        logger.error(f"{cmd[0]} exited with returncode {e.returncode} \n{e.stderr.decode()}")
        raise SystemExit(e.returncode)


def parse_iso_date(date_str):
    try:
        dt = dateutil.parser.parse(date_str)
        return dt.date().isoformat()
    except (ParserError, TypeError) as e:
        logger.warning(f"invalid date string: '{date_str}'")


def parse_TDAT_tag(tag_tdat):
    try:
        iso_date_str = tag_tdat.split(' ')[0]
        return parse_iso_date(iso_date_str)
    except (AttributeError, IndexError) as e:
        logger.debug(f"invalid 'TDAT' tag: '{tag_tdat}'")
        return None


def get_iso_date_in_file(file_path):
    tags = ffprobe_get_tags(file_path)

    tag_TDAT = tags.get("TDAT")
    tag_date = tags.get("date")

    parsed_TDAT = parse_TDAT_tag(tag_TDAT)
    parsed_date = parse_iso_date(tag_date)

    if parsed_TDAT is None and parsed_date is None:
        logger.error(f"no valid date found in '{file_path}' - TDAT: '{tag_TDAT}', date: '{tag_date}'")
        raise SystemExit(3)

    else:
        logger.debug(f"TDAT: '{parsed_TDAT}' ('{tag_TDAT}'), date: '{parsed_date}' ('{tag_date}')")
        logger.debug(f"date: {parsed_date}")

    if parsed_TDAT != parsed_date:
        logger.debug(f"dates in 'TDAT' ({parsed_TDAT}) and 'date' ({parsed_date}) differ!")

    if parsed_date is not None:
        return parsed_date
    else:
        return parsed_TDAT


def file_dates_are_ok(file_path):
    tags = ffprobe_get_tags(file_path)
    tag_date = tags.get("date")
    try:
        dt = datetime.fromisoformat(tag_date)
        ts = time.mktime(dt.timetuple())
        os.stat(file_path).st_mtime == ts
    except ValueError:
        return False

def set_utime(file_path, iso_date_str):
    dt = dateutil.parser.parse(iso_date_str)
    ts = time.mktime(dt.timetuple())
    # shutil.move(file_path, f"{file_path}.new")
    # shutil.move(f"{file_path}.new", file_path)
    os.utime(file_path, (ts, ts))
    try:
        os.utime(os.path.dirname(file_path), (ts, ts))
    except FileNotFoundError:
        pass
    return dt


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("podcast_file")
    parser.add_argument("--out-file", default="/tmp/out-{os.getpid()}.mp3")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--ffmpeg", action="store_true")
    parser.add_argument("--mtime", action="store_true", help="only set mtime, no mp3 metadata")
    parser.add_argument("--fix-album-tag", action="store_true", help="write album tag (podcast name)")
    parser.add_argument("--podcast-name")
    args = parser.parse_args()

    if not args.debug:
        logger.remove()

        if args.quiet:
            logger.add(sys.stderr, level="ERROR")
        else:
            logger.add(sys.stderr, level="INFO")

    return args


def main():
    args = parse_args()
    logger.debug(f"checking: '{os.path.basename(args.podcast_file)}'")

    if args.fix_album_tag:
        podcast_name = get_podcast_name_from_dir(args.podcast_file)
        if podcast_name is not None:
            eyeD3_write_album_tag(args.podcast_file, podcast_name)
            logger.info(f"set album tag to '{podcast_name}' for '{args.podcast_file}'")


    date = get_iso_date_in_file(args.podcast_file)

    if args.mtime:
        dt = set_utime(args.podcast_filen, date)
        logger.info(f"set mtime for '{os.path.basename(args.podcast_file)}' to '{dt.isoformat()}' according to mp3 metadata")

    elif file_dates_are_ok(args.podcast_file):
        logger.info(f"metadata date and filesystem utimes ar ok for {args.podcast_file}', did not modify file")
    else:
        if args.ffmpeg:
            ffmpeg_write_date_tag(args.podcast_file, args.out_file, date)
        else:
            eyeD3_write_date_tag(args.podcast_file, date)

        set_utime(args.podcast_file, date)
        logger.success(f"updated date in '{args.podcast_file}' as {date}")



if __name__ == "__main__":
    main()
