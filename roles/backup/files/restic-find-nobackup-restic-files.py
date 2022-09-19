#!/bin/bash

# find .. -name .nobackup.restic -exec dirname {} \;

TMPFILE=/tmp/restic-paths.txt
touch $TMPFILE
echo > $TMPFILE

{% for repo in restic_config -%}
{% for p in restic_config[repo].paths -%}
find {{ p.path }} -name ".nobackup.restic" >> $TMPFILE
{% endfor %}
{% endfor %}

cat $TMPFILE | sort -u > /usr/local/var/restic-nobackup.conf
