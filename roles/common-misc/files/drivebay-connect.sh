#!/bin/bash

set -e

echo '4-2' > /sys/bus/usb/drivers/usb/bind

echo -n "waiting for drives"

for i in {0..300}
do
  if [[ -b "/dev/sdb" && -b "/dev/sdc" ]]; then
    echo " [ ok ]"
    lsblk | egrep "^sd[a-z]"
    exit 0
  else
    echo -n "."
    sleep 3
  fi
done

echo "sdb and/or sdc not found"
exit 1
