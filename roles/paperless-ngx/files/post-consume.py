#!/usr/bin/env python3

from common_consume import logger


def main():
    post_consume_vars = [
        "DOCUMENT_ID",
        "DOCUMENT_FILE_NAME",
        "DOCUMENT_CREATED",
        "DOCUMENT_MODIFIED",
        "DOCUMENT_ADDED",
        "DOCUMENT_SOURCE_PATH",
        "DOCUMENT_ARCHIVE_PATH",
        "DOCUMENT_THUMBNAIL_PATH",
        "DOCUMENT_DOWNLOAD_URL",
        "DOCUMENT_THUMBNAIL_URL",
        "DOCUMENT_CORRESPONDENT",
        "DOCUMENT_TAGS",
        "DOCUMENT_ORIGINAL_FILENAME"
    ]
    logger(post_consume_vars, "post")


if __name__ == "__main__":
    main()
