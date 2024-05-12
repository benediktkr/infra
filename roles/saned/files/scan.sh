#!/bin/bash

set -e

# scanimage --source="ADF Duplex" -d $SCANBD_DEVICE --page-width 215.9 --page-height 355.6 -y 355.6 -x 215.9 --batch --format=tiff --mode Lineart --resolution 300 

# Links:
#  https://askubuntu.com/questions/106769/scanning-from-terminal#106776
#  https://unix.stackexchange.com/questions/393270/how-do-i-automatically-scan-documents-on-linux-from-the-terminal


date=$(date -I)
if [[ -n "$1" ]]; then
    scan_name=$1
    filename="${date}_${scan_name}.pdf"
else
    filename="${date}.pdf"
fi

if [[ -f "${filename}" ]]; then
    echo "File '${filename}' already exists, renaming it"
    mv_uuid=$(uuidgen | awk -F'-' '{ print $1 }')
    mv_basename=$(basename -- "${filename}" ".${filename##*.}")
    mv -v ${filename} ${mv_basename}-${mv_uuid}.pdf
fi


#  -x 210 -y 297 
# DPI is set with --resolution
# A4 is 210x297mm

sudo scanimage --resolution 300 --output-file=${filename}


user=$(id -u)
group=$(id -g)
sudo chown ${user}:${group} $filename
ls --color=always -lh $filename

