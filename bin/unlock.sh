#!/bin/bash

set -e

source ~/.config/luks.env

ssh ${1}-initramfs "echo -ne $LUKS > /lib/cryptsetup/passfifo"

