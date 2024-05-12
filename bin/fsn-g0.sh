#!/bin/bash

set -e

ansible fsn-g0.sudo.is -m service -a "name=nginx state=restarted"

# "stale file handle" on clients
# https://unix.stackexchange.com/questions/433051/mount-nfs-stale-file-handle-error-cannot-umount
#
# sudo umount -l /deadspace/video/movies
# sudo systemctl start deadspace-video-movies.mount
ansible fsn-g0.sudo.is -m command -a "cat /proc/fs/nfs/exports"
ansible fsn-g0.sudo.is --become -m command -a "exportfs -ua"
ansible fsn-g0.sudo.is --become -m command -a "exportfs -a"

#ansible-playbook pirate.yml --diff --limit fsn-g0.sudo.is --tags docker-containers,docker-container,transmission-container,transmission-containers
ansible-playbook site2.yml --diff --limit fsn-g0.sudo.is --tags docker-containers,docker-container,transmission-container,transmission-containers

ansible fsn-g0.sudo.is -m command -a "cat /proc/fs/nfs/exports"


