resource "digitalocean_volume" "docker-nextcloud" {
  region = "ams3"
  name   = "docker-nextcloud"
  size   = 10

  /*
   * ADD LIFECYCLE PROTECTION
   */

}

resource "digitalocean_droplet" "docker" {
  image              = "ubuntu-18-04-x64"
  name               = "docker"
  region             = "ams3"
  size               = "s-1vcpu-2gb"
  monitoring         = true
  ipv6               = true
  private_networking = true
  resize_disk        = false
  ssh_keys           = ["cb:79:d0:73:55:b1:79:60:a4:a9:d5:48:53:e2:67:13"]
  volume_ids         = ["${digitalocean_volume.docker-nextcloud.id}"]
}

resource "digitalocean_record" "docker" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "A"
  ttl    = 60
  name   = "${digitalocean_droplet.docker.name}"
  value  = "${digitalocean_droplet.docker.ipv4_address}"
}

resource "digitalocean_record" "docker-local" {
  domain = "${digitalocean_domain.sudo-local.name}"
  type   = "A"
  ttl    = 60
  name   = "${digitalocean_droplet.docker.name}"
  value  = "${digitalocean_droplet.docker.ipv4_address_private}"
}

resource "digitalocean_record" "docker6" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "AAAA"
  ttl    = 60
  name   = "${digitalocean_droplet.docker.name}"
  value  = "${digitalocean_droplet.docker.ipv6_address}"
}

output "docker-ip" {
  value = "${digitalocean_droplet.docker.ipv4_address}"
}
