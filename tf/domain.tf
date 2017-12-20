variable "domain" {
  default = "do.sudo.is"
}

resource "digitalocean_domain" "do-sudo-is" {
  name = "${var.domain}"
  ip_address = "${digitalocean_droplet.lon-vpn.ipv4_address}"    # required
}

