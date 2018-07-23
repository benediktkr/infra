# Plan

* 1 util node (`mathom`)
    - volume for `/home` for persistence
* 1 docker node
    - nextcloud (with volume `docker-nextcloud`)
    - bitcoin-lnd
    - cv
    - sudo.is webpage
* 1 mail node
* 1 vpn node

# Droplets

## mathom

things

## docker

First built with these parameters to get a 25gb disk

```
size        = "s1-1vcpu-1gb"
resize_disk = false
```

Then it's resized to a `s1-1vcpu-2gb` to get 2gb of ram and still keep 25gb disk.

# Rebuilding nodes

Design choice: Should tolerate being rebuilt every now and then (e.g. OS updates). All persistent data will be on LUKS encrypted volumes. This section will document that process.

# LUKS Volumes (without LVM)

Guide to resizing LUKS volumes

## Creating

This is how the LUKS volumes are created

```shell
# TF_NAME=mathom-home
# DO_DEVICE=/dev/disk/by-id/scsi-0DO_Volume_$TF_NAME
```

```shell
# cryptsetup luksFormat --cipher aes-xts-plain64 -s 256 --iter-time 6000 $DO_DEVICE
Enter passphrase:
# cryptsetup luksOpen $DO_DEVICE mathom-home
Enter passphrase:
# mkfs.ext4 /dev/mapper/mathom-home
#
```

## Resizing

First, resize in the DO web interface. Currently it does not seem to work in terraform, it wants to recreate the volume.

```shell
# cryptsetup luksClose /dev/mapper/$TF_NAME
# cryptsetup luksOpen /dev/disk/by-id/$DO_DEVICE mathom-home
Enter passphrase:
# lsblk
  [ See new size ? ]
# e2fsck -f /dev/mapper/mathom-home
# resize2fs /dev/mapper/mathom-home
#
```

# Internal dns

The zone `sudo.local` is hosted in the DigitalOcean DNS manager. Each droplet has a `$name.sudo.local` record pointing to it's internal IP address.

Questions:

1. Does this internal IP ever change?

2. What if another account tries to resolve this domain?
