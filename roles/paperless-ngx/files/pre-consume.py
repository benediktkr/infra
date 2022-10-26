#!/usr/bin/env python3

from common_consume import logger


def main():
    pre_consume_vars = [
        "DOCUMENT_SOURCE_PATH"
    ]
    logger(pre_consume_vars, "pre")


if __name__ == "__main__":
    main()
