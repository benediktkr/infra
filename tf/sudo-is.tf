### sudo.is
resource "digitalocean_domain" "sudo-is" {
  name = "sudo.is"
  ip_address = "${local.freespace_ip}"
}

# MX sudo.is
resource "digitalocean_record" "sudo-is-mx-0" {
  domain   = "${digitalocean_domain.sudo-is.name}"
  type     = "MX"
  name     = "@"
  priority = "10"
  value    = "freespace.sudo.is."
  ttl      = 60
}

# TXT
resource "digitalocean_record" "sudo-is-txt" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "TXT"
  name   = "@"
  value  = "v=spf1 mx a ptr ip4:${local.freespace_ip}/32 include=_spf.investici.org"
  ttl    = 60
}
