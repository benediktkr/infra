#!/bin/bash
#

set -e

usage() {
    echo "usage: $0 [--limit LIMIT|--dry-run|--debug|--help]"
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
            SHOW_ENV="true"
            DEBUG="true"
            ;;
        --dry-run)
            shift
            SHOW_ENV="true"
            DRY_RUN="true"
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

echo    "Limit...: \"${GROUPS_LIMIT}\""
echo    "Groups..: "
for item in ${CONVERGENCE_GROUPS}; do
    echo "  - ${item}"
done

if [[ "${SHOW_ENV}" == "true" ]]; then
    echo "Env....: "
    env | grep ANSIBLE | sed 's/^/  /g'
fi

if [[ "${DRY_RUN}" == "true" ]]; then
    echo
    echo "Exiting without running Ansible."
    exit 0
fi

if [[ "${DEBUG}" == "true" ]]; then
    set -x
fi
ansible-playbook common.yml --check --diff --limit ${GROUPS_LIMIT}
for item in ${CONVERGENCE_GROUPS}; do
    ansible-playbook ${item}.yml --diff --check
done



# ansible-playbook common.yml --limit mathom --diff --check
# ansible-playbook common.yml --check --diff --limit hass,mathom,edge

