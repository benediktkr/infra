# Plan

* 1 util node (`mathom`)
    - volume for `/home` for persistence
    - vpn client to vpn.sudo.is to provide inter-region private networks
    - Set IP network for private network:
       https://www.digitalocean.com/docs/networking/private-networking/how-to/enable/#ubuntu-18-04
    - Should maybe house mail server too.
* 1 docker node
    - nextcloud (with volume `docker-nextcloud`)
    - bitcoin-lnd
    - cv
    - sudo.is webpage
* 1 mail node
* 1 vpn node, in london. already exists but needs to be rebuilt

# Costs

##Only using 1 vcpu nodes

```
mathom 1gb         -  $5
mail 1gb           -  $5
vpn 1gb            -  $5
docker 2gb         - $10
---
Total:               $30
```

Using a mix of 1vcp and 2vcp

```
vpn 1vcp 1gb:      $5
mathom 2vcpu 2gb   $15
docker 2vcpu 2gb   $15
---
Total              $35

mail 1vcpu 1gb     $5
---
Total with mail    $40
```

# Droplets

## mathom

Will be a collection of system-level things, and used as a remote
shell by me. The name comes from Lord of the Rings and has been used
by me for various computers that have fitted the LotR word.

# Getting a smaller root volume

First build with these parameters to get a 25gb disk

```
size        = "s1-1vcpu-1gb"
resize_disk = false
```

Then it's resized to a `s1-1vcpu-2gb` to get 2gb of ram and still keep 25gb disk.

# Rebuilding nodes

Design choice: Should tolerate being rebuilt every now and then (e.g. OS updates). All persistent data will be on LUKS encrypted volumes. This section will document that process.

# Provisioning

Use ansible in this repo. Use the DO inventory script.

# LUKS Volumes (without LVM)

Guide to resizing LUKS volumes

## Creating

This is how the LUKS volumes are created

```console
# TF_NAME=mathom-home
# DO_DEVICE=/dev/disk/by-id/scsi-0DO_Volume_$TF_NAME
```

```console
# cryptsetup luksFormat --cipher aes-xts-plain64 -s 256 --iter-time 6000 $DO_DEVICE
Enter passphrase:
# cryptsetup luksOpen $DO_DEVICE mathom-home
Enter passphrase:
# mkfs.ext4 /dev/mapper/mathom-home
#
```

## Resizing

First, resize in the DO web interface. Currently it does not seem to work in terraform, it wants to recreate the volume.

```console
# cryptsetup luksClose /dev/mapper/$TF_NAME
# cryptsetup luksOpen /dev/disk/by-id/$DO_DEVICE mathom-home
Enter passphrase:
# lsblk
  [ See new size ? ]
# e2fsck -f /dev/mapper/mathom-home
# resize2fs /dev/mapper/mathom-home
#
```

See also: https://wiki.archlinux.org/index.php/Resizing_LVM-on-LUKS

# Internal dns

The zone `sudo.local` is hosted in the DigitalOcean DNS manager. Each droplet has a `$name.sudo.local` record pointing to it's internal IP address.

Questions:

1. Does this internal IP ever change?

2. What if another account tries to resolve this domain?
   The ns{1..5}.digitalocean.com servers will try to resolve them as a normal
   recursive resolver.
