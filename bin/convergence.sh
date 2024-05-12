#!/bin/bash
#

set +e
set -x


export ANSIBLE_STDOUT_CALLBACK="debug"
export ANSIBLE_DISPLAY_SKIPPED_HOSTS="false"
export ANSIBLE_DISPLAY_OK_HOSTS="false"


# ansible-playbook common.yml --limit mathom --diff --check
ansible-playbook common.yml --check --diff --limit hass,mathom,edge

for item in hass mathom edge; do
    ansible-playbook ${item}.yml --diff --check
done
