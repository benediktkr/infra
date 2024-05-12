#!/bin/bash

du_sh() {
    ansible "${oldhost},${newhost}" -m command -a "du -sh $rsync_path"
}

if [[ -z "$oldhost" || -z "$newhost" ]]; then
    echo "please set 'oldhost' and 'newhost'."
    exit 2
fi

if [[ -z "$1" ]]; then
    echo "usage: $0 PATH"
    exit 1
else
    rsync_path=$1
fi

extra_var="{
   \"srchost\":\"${oldhost}\",
   \"dsthost\":\"${newhost}\",
   \"paths\": [\"${rsync_path}\"]
}"

echo $extra_var | jq .
du_sh

read -p "Continue? Press any key. " FOO

ansible-playbook private/playbooks/rsync-paths.yml -e "$extra_var"

du_sh

