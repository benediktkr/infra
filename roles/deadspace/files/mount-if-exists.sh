#!/bin/bash

set -e

if [[ -z "$1" && -z "$2" ]]; then
    echo "$0 <name> <mountpoint>"
    exit 1
fi

NAME=$1
MOUNTPOINT=$2
 
if [[ $(findmnt -M $MOUNTPOINT) ]]; then
    echo "already mounted: '${MOUNTPOINT}'"
    exit 0
elif [[ ! -b "/dev/mapper/$NAME" ]]; then
    echo "not mounting: '/dev/mapper/$NAME' doesn't exist"
    exit 0
fi

mount -v /dev/mapper/$NAME $MOUNTPOINT
echo "mounted $NAME"
exit 0

