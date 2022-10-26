#!/usr/bin/env python3

import json
from os import environ, path
from datetime import datetime

DATA_DIR = environ.get("PAPERLESS_DATA_DIR", "../data/")
LOGGING_DIR = environ.get("PAPERLESS_LOGGING_DIR", path.join(DATA_DIR, "log/"))


def logger(env_vars, consume_stage):
    # paperless-ngx has a hardcoded log file name anyay
    log_path = path.join(LOGGING_DIR, "consume.log")

    log_item = {k.lower(): environ.get(k) for k in env_vars}
    log_item.update({
        "timestamp": datetime.now().isoformat(),
        "paperless_user": environ.get("PAPERLESS_USER"),
        "log_path": log_path,
        "paperless_consume_stage": consume_stage

    })

    with open(log_path, 'a') as f:
        #j = json.dumps(log_item, indent=2)
        j = json.dumps(log_item)
        f.write(j)
        f.write("\n")
