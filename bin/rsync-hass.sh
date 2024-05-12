#!/bin/bash

set -e

oldhost="ber-hass-b0.s21.sudo.is"
newhost="ber-hass0.s21.sudo.is"
rsync_path="/srv/hass/"

extra_var="{
   \"srchost\":\"${oldhost}\",
   \"dsthost\":\"${newhost}\",
   \"paths\": [\"${rsync_path}\"]
}"

echo $extra_var | jq .


ansible "${oldhost}" -m command -a "du -sh {{systemuserlist.hass.home}}"
ansible "${newhost}" -m command -a "du -sh {{systemuserlist.hass.home}}"

ansible-playbook private/playbooks/rsync-paths.yml -e "$extra_var"


ansible $newhost -m command -a "du -sh {{systemuserlist.hass.home}}"
