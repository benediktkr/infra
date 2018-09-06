#!/bin/bash

apt-add-repository ppa:ansible/ansible
apt-get update
apt-get install -y git software-properties-common ssh ansible
mkdir -p /root/.ssh/
cp ansible/roles/common/files/id_rsa.pub /root/.ssh/authorized_keys
chmod -R 700 /root/.ssh/
