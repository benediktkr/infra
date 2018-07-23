# Plan

* 1 util node (`mathom`)
  * Volume for `/home` for persistence
* 1 docker node
  * nextcloud (with volume `docker-nextcloud`)
  * bitcoin-lnd
  * cv
  * sudo.is webpage
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

Should tolerate being rebuilt every now and then (e.g. OS updates). All persistent data will be on LUKS encrypted volumes. This section will document that process.

# Expanding Volumes

Guide to resizing LUKS encrypted volumes

# Internal dns

The zone `sudo.local` is hosted in the DigitalOcean DNS manager. Each droplet has a `$name.sudo.local` record pointing to it's internal IP address.

Questions:
1. Does this internal IP ever change?
2. What if another account tries to resolve this domain?
