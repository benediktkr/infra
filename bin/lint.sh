#!/bin/sh

echo "output is currently redirected to /dev/null"

yamllint $1 &>/dev/null

returncode=$?
echo "yamllint returncode: $returncode"

exit 0
