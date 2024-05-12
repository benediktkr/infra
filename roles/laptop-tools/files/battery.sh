#!/bin/bash

BAT0=$(upower --show-info /org/freedesktop/UPower/devices/battery_BAT0 | grep percentage | awk '{ print $2 }')
BAT1=$(upower --show-info /org/freedesktop/UPower/devices/battery_BAT1 | grep percentage | awk '{ print $2 }')
AC=$(cat /sys/class/power_supply/AC/online)

echo '{'

echo -ne '    "BAT0": "'
echo -ne "${BAT0}"
echo '",'

echo -ne '    "BAT1": "'
echo -ne "${BAT1}"
echo '",'

echo -ne '    "AC": '
if [[ "$AC" == "1" ]]; then
    echo "true"
else
    echo "false"
fi
echo '}'

