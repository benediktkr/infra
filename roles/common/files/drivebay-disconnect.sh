#!/bin/bash

set -e

echo '4-2' > /sys/bus/usb/drivers/usb/unbind
lsblk | egrep "^sd[a-z]"
