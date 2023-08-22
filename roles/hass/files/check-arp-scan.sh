#!/bin/bash

set -e

ARP_FILE=$(find /tmp/arp-scan.txt -mmin -1 2>/dev/null)

echo $1 > /tmp/check-arp-scan-args.txt

[[ -z "$1" ]] && exit 1
[[ -f "/tmp/arp-scan.txt" ]] || exit 1
[[ -z "$ARP_FILE" ]] && exit 1

if `grep -qF $1 $ARP_FILE`; then
    echo "ON"
else
    echo "OFF"
fi

exit 0
