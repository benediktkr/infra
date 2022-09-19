#!/bin/bash

set -e
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

if [[ "$2" = "--dry-run" ]]; then
    DRY_RUN="--dry-run"
    echo "--- BEGIN WARNING -----"
    echo
    echo "this is a DRY RUN!"
    echo
    echo "to do a real run, use:"
    echo "$0 $1 --ok"
    echo
    echo
    echo "--- END WARNING -------"
    echo
    echo
else
    DRY_RUN=""
fi

OLD_HOST_NAME=$1
DEST_DIR="/deadspace/local/old-hosts/${OLD_HOST_NAME}/"

RSNAPSHOT_HOST="freespace.vpn.sudo.is"
SRC_DIR="/deadspace/backups/rsnapshot/alpha.0/${OLD_HOST_NAME}/"

echo "hostname: ${OLD_HOST_NAME}"
echo "destination: ${DEST_DIR}"
echo "source: ${RSNAPSHOT_HOST}:${SRC_DIR}"
echo

echo "remote size:"
echo -ne "${OLD_HOST_NAME}\t"
ssh $RSNAPSHOT_HOST -- du -sh ${SRC_DIR} | awk '{print $1}'
echo

rsync -rah $DRY_RUN \
  --numeric-ids \
  --info=progress2 \
  root@${RSNAPSHOT_HOST}:${SRC_DIR} \
  ${DEST_DIR}

if [[ "$DRY_RUN" == "" ]]; then
    echo
    echo -ne "local size:\t"
    du -sh ${DEST_DIR} | awk '{print $1}'
fi

echo
echo "cleanup, on ${RSNAPSHOT_HOST} and hosts that sync the rsnapshot with deadspace:"
echo " rm -rf ${SRC_DIR}"
echo
