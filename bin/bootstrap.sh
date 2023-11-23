#!/bin/bash
#ssh -o "UserKnownHostsFile=/dev/shm/knownhosts" $1 bash -c "
    curl https://www.sudo.is/ben.pub > /tmp/authorized_keys && \
    sudo mkdir -p /root/.ssh/ && \
    sudo cp  /tmp/authorized_keys /root/.ssh/authorized_keys && \
    sudo chmod -R 700 /root/.ssh && \
    sudo chown -R root:root /root/.ssh && \
    sudo useradd -d /var/lib/ansible -u 2000 -m -G sudo ansible && \
    sudo mkdir -p /var/lib/ansible/.ssh && \
    sudo cp /tmp/authorized_keys /var/lib/ansible/.ssh/authorized_keys
    sudo chown -R ansible:ansible /var/lib/ansible/.ssh && \
    sudo chmod -R 700 /var/lib/ansible/.ssh && \
    rm /tmp/authorized_keys
#"
