#!/usr/bin/env python3

import argparse
from datetime import datetime, date, timedelta
import subprocess
import json
import sys
import os
import time

import eyed3
from loguru import logger
import dateutil.parser
from dateutil.parser._parser import ParserError
from mutagen.id3 import ID3


def delete_file(file_path):
    try:
        os.remove(file_path)
        logger.debug(f"deleted: '{file_path}'")
    except FileNotFoundError:
        pass


def replace_file(src, dest):
    try:
        logger.debug(f"src: {src}, dest: {dest}")
        os.replace(src, dest)
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
        "-c",  "copy",
        "-metadata",  f"date={iso_date_str}",
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
    cmd = [
        "eyeD3",
        "--release-date", iso_date_str,
        "--to-v2.4",
        "--user-text-frame", f"releasedate:{iso_date_str}",
        # "--preserve-file-times",
        # "--recording-date", iso_date_str,
        # "--orig-release-date", iso_date_str,
        podcast_file
    ]

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
    if date_str is None:
        return None

    try:
        dt = dateutil.parser.parse(date_str)
        return dt.date().isoformat()
    except (ParserError, TypeError) as e:
        logger.warning(f"invalid date string: '{date_str}'")
        return None


def parse_TDAT_tag(tag_tdat, tag_tyer):
    if tag_tdat is None:
        return None
    if tag_tyer is None:
        return None
    if not isinstance(tag_tdat, str) or len(tag_tdat) != 4:
        return None
    if not isinstance(tag_tyer, str) or len(tag_tyer) != 4:
        return None


    # TDAT is id3 v2.3: DDMM
    # TYER is id3 v2.3: YYYY
    try:
        #iso_date_str = tag_tdat.split(' ')[0]
        #return parse_iso_date(iso_date_str)
        DD = tag_tdat[0:2]
        MM = tag_tdat[2:4]
        YYYY = tag_tyer[0:4]
        isofmt = f"{YYYY}-{MM}-{DD}"
        if is_iso_string(isofmt):
            return isofmt
        else:
            logger.warning(f"invalid TDAT: {tag_tdat} and TYER: {tag_tyer}")
            return None
    except (AttributeError, IndexError) as e:
        logger.debug(f"invalid 'TDAT' tag: '{tag_tdat}'")
        return None


def is_iso_string(iso_string):
    if iso_string is None:
        return False
    try:
        datetime.fromisoformat(iso_string)
        return True
    except ValueError:
        return False

def get_iso_date_in_file(file_path):
    tags = ffprobe_get_tags(file_path)
    l = []

    # print(tag_tdat)
    # print(tag_tyer)
    for item in ["releasedate", "date"]:
        parsed = parse_iso_date(tags.get(item))
        if is_iso_string(parsed):
            l.append(parsed)


    tag_tdat = tags.get("TDAT")
    tag_tyer = tags.get("TYER")
    if len(l) == 0 and (tag_tdat is not None and tag_tyer is not None):
        logger.info(f"TDAT: {tag_tdat}")
        logger.info(f"TYER: {tag_tyer}")
        tdat = parse_TDAT_tag(tag_tdat, tag_tyer)
        if is_iso_string(tdat):
                l.append(tdat)


    dates = set(l)
    if len(dates) == 0:
        logger.error(f"no valid date found for '{file_path}'")
        raise SystemExit(3)


    elif len(dates) == 1:
        d = list(dates)[0]
        logger.debug(f"date found: {d}")
        return d

    else:
        logger.info(f"multiple dates found: {dates}, picking earliest")
        earliest = min([datetime.fromisoformat(a) for a in dates])
        return earliest.isoformat()


def get_iso_date_in_file2(file_path):
    tags = ffprobe_get_tags(file_path)

    tag_TDAT = tags.get("TDAT")
    tag_date = tags.get("date")
    #tag_releasedate = tags.get("releasedate")

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

def st_time_to_iso(st_time):
    return datetime.fromtimestamp(st_time).isoformat()

def show_info(file_path):
    statinfo = os.stat(file_path)

    atime = st_time_to_iso(statinfo.st_atime)
    mtime = st_time_to_iso(statinfo.st_mtime)
    ctime = st_time_to_iso(statinfo.st_ctime)
    logger.info(f"atime: {atime}")
    logger.info(f"mtime: {mtime}")
    logger.info(f"ctime: {ctime}")


def set_utime(file_path, iso_date_str):
    # settings access and modified times
    dt = dateutil.parser.parse(iso_date_str)
    ts = time.mktime(dt.timetuple())
    os.utime(file_path, (ts, ts))
    try:
        os.utime(os.path.dirname(file_path), (ts, ts))
    except FileNotFoundError:
        pass
    return dt

def eyed3_dates(podcast_file, date_str):
    a = eyed3.load(podcast_file)


def mutagen_dates(podcast_file, date_str):
    id3 = ID3(podcast_file)
    print(type(id3))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["show", "utime-only", "fix-dates", "fix-album-tag"])
    parser.add_argument("--podcast-file")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--ffmpeg-out-file", default=f"/tmp/out-{os.getpid()}.mp3")
    parser.add_argument("--metadata-util", default="eyed3", choices=["mutagen", "eyeD3", "ffmpeg"], type=str.lower)
    parser.add_argument("--utime-only", action="store_true", help="only set utime, no mp3 metadata")
    parser.add_argument("--podcast-name")
    args = parser.parse_args()

    LOG_FORMAT = " ".join([
        "<green><dim>{time:YYYY-MM-DDT}</dim>{time:HH:mm}<dim>{time:Z}</dim></green>",
        "<dim><level>{level: >8}</level></dim>",
        "<level>{message}</level>"
    ])

    if not args.debug:
        logger.remove()

        if args.quiet:
            logger.add(sys.stderr, level="ERROR", format=LOG_FORMAT)
        else:
            logger.add(sys.stderr, level="INFO", format=LOG_FORMAT)
    return args


def main():
    args = parse_args()
    logger.debug(f"checking: '{os.path.basename(args.podcast_file)}'")

    podcast_date = get_iso_date_in_file(args.podcast_file)

    if args.action == "show":
        show_info(args.podcast_file)

    if args.action == "utime-only":
        dt = set_utime(args.podcast_file, podcast_date)
        logger.info(f"set mtime for '{os.path.basename(args.podcast_file)}' to '{dt.isoformat()}' according to mp3 metadata")

    if args.action == "fix-dates":
        if args.metadata_util == "ffmpeg":
            ffmpeg_write_date_tag(args.podcast_file, args.out_file, podcast_date)
        if args.metadata_util == "eyed3":
            eyeD3_write_date_tag(args.podcast_file, podcast_date)
            eyed3_dates(args.podcast_file, podcast_date)
        if args.metadata_util == "mutagen":
            mutagen_dates(args.podcast_file, podcast_date)


        _today = date.today()
        _yesterday = date.today() - timedelta(days=1)
        if datetime.fromisoformat(podcast_date).date() == _today:
            utime = datetime.now() - timedelta(hours=1)
            utime_iso = utime.isoformat()
            set_utime(args.podcast_file, utime_iso)
        else:
            set_utime(args.podcast_file, podcast_date)

        logger.debug(f'updated podcast_file="{args.podcast_file}" podcast_date="{podcast_date}"')
        ep_name = os.path.basename(args.podcast_file)
        podcast_name = os.path.basename(os.path.dirname(args.podcast_file))
        logger.success(f'podcast_name="{podcast_name}" ep_name="{ep_name}" podcast_date="{podcast_date}"')

    if args.action == "fix-album-tag":
        podcast_name = get_podcast_name_from_dir(args.podcast_file)
        if podcast_name is not None:
            eyeD3_write_album_tag(args.podcast_file, podcast_name)
            logger.info(f"set album tag to '{podcast_name}' for '{args.podcast_file}'")


if __name__ == "__main__":
    main()
