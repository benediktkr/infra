#!/bin/bash
#

set +e

usage() {
    echo "usage: $0 [--limit LIMIT|--help|--debug]"
}

for arg in "$@"; do
    case $arg in
        -h|--help)
            usage
            exit 1
            ;;
        --limit)
            shift
            LIMIT=$1
            shift
            export LIMIT
            ;;
        --debug)
            shift
            set -x
            ;;
        *)
            usage
            echo "unkonwn arg: '$1'"
            #exit 3
    esac
done


export ANSIBLE_STDOUT_CALLBACK="debug"
export ANSIBLE_DISPLAY_SKIPPED_HOSTS="false"
export ANSIBLE_DISPLAY_OK_HOSTS="false"

if [[ -n "$LIMIT" ]]; then
    CONVERGENCE_GROUPS=$LIMIT
    GROUPS_LIMIT=$LIMIT
else
    CONVERGENCE_GROUPS="hass mathom edge"
    GROUPS_LIMIT=$(echo $CONVERGENCE_GROUPS | tr ' ' ',')
fi

ansible-playbook common.yml --check --diff --limit ${GROUPS_LIMIT}
for item in ${CONVERGENCE_GROUPS}; do
    ansible-playbook ${item}.yml --diff --check
done



# ansible-playbook common.yml --limit mathom --diff --check
# ansible-playbook common.yml --check --diff --limit hass,mathom,edge

