#!/bin/bash

BAT0=$(upower --show-info /org/freedesktop/UPower/devices/battery_BAT0 | grep percentage | awk '{ print $2 }')
BAT1=$(upower --show-info /org/freedesktop/UPower/devices/battery_BAT1 | grep percentage | awk '{ print $2 }')

echo '{'

echo -ne '    "BAT0": "'
echo -ne "${BAT0}"
echo '",'

echo -ne '    "BAT1": "'
echo -ne "${BAT1}"
echo '"'
echo '}'

