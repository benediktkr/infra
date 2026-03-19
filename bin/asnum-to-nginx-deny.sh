#!/bin/bash

if [[ -z "$1" ]]; then
    echo "usage: $0 <ASNUM> [-h]"
    exit 1
else
    ASNUM=$1
    shift
fi

BLOCKLIST_D=${HOME}/infra/private/roles/nginx/files/blocklists.d
OUTPUT_FILE=${BLOCKLIST_D}/${ASNUM}.conf

if [[ -f "${OUTPUT_FILE}" ]]; then
    echo "already exists: '${ASNUM}.conf'"
    echo -n "entries: "
    wc -l ${OUTPUT_FILE} | awk '{ print $1 }'
    echo "exiting without overwriting!"
    exit 2
fi

whois -h whois.radb.net -- "-i origin ${ASNUM}"  |
    grep 'route:' |
    awk '{ print "deny ", $2, ";" }' |
    sort -u > ${OUTPUT_FILE}

echo "wrote: '${ASNUM}.conf'"
echo -n "entries: "
wc -l ${OUTPUT_FILE} | awk '{ print $1 }'
