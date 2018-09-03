resource "digitalocean_volume" "mathom-home" {
  region = "ams3" # "${digitalocean_droplet.mathom.region}"
  name   = "mathom-home"
  size   = 11

  /*
   * ADD LIFECYCLE PROTECTION
   */

}

resource "digitalocean_droplet" "mathom" {
  image              = "ubuntu-18-04-x64"
  name               = "mathom"
  region             = "ams3"
  size               = "s-1vcpu-1gb"
  monitoring         = true
  ipv6               = true
  private_networking = true
  resize_disk        = false
  ssh_keys           = ["cb:79:d0:73:55:b1:79:60:a4:a9:d5:48:53:e2:67:13"]
  volume_ids         = ["${digitalocean_volume.mathom-home.id}"]
}

resource "digitalocean_record" "mathom" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "A"
  ttl    = 60
  name   = "${digitalocean_droplet.mathom.name}"
  value  = "${digitalocean_droplet.mathom.ipv4_address}"
}

resource "digitalocean_record" "mathom6" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "AAAA"
  ttl    = 60
  name   = "${digitalocean_droplet.mathom.name}"
  value  = "${digitalocean_droplet.mathom.ipv6_address}"
}

resource "digitalocean_record" "mathom-local" {
  domain = "${digitalocean_domain.sudo-local.name}"
  type   = "A"
  ttl    = 60
  name   = "${digitalocean_droplet.mathom.name}"
  value  = "${digitalocean_droplet.mathom.ipv4_address_private}"
}



output "mathom-ip" {
  value = "${digitalocean_droplet.mathom.ipv4_address}"
}

output "mathom-home" {
  value = "${digitalocean_volume.mathom-home.id}"
}
