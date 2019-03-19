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
  value  = "v=spf1 mx a ptr ip4:${local.freespace_ip}/32 ip4:${local.endor_ip} include=_spf.investici.org"
  ttl    = 60
}

# CNAME www.sudo.is
resource "digitalocean_record" "www-sudo-is" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "CNAME"
  name   = "www"
  value  = "${digitalocean_domain.sudo-is.name}."
  ttl    = 60
}

# f.sudo.is (firstroot)
resource "digitalocean_record" "f-sudo-is" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "A"
  name   = "f"
  value  = "${local.f_ip}"
  ttl    = 60
}



# freespace.sudo.is
resource "digitalocean_record" "freespace-sudo-is" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "A"
  name   = "freespace"
  value  = "${local.freespace_ip}"
  ttl    = 60
}

# endor.sudo.is
resource "digitalocean_record" "endor-sudo-is" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "A"
  name   = "endor"
  value  = "${local.endor_ip}"
  ttl    = 60
}

# CNAMEs to freespace
locals {
  freespace_cnames = [
    "benedikt",
    "static",
    "notes",
    "nextcloud",
    "de-vpn"
  ]
}

resource "digitalocean_record" "freespace-cnames" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "CNAME"
  name   = "${element(local.freespace_cnames, count.index)}"
  count  = "${length(local.freespace_cnames)}"
  value  = "freespace.sudo.is."
  ttl    = 60

}

# eyjabakki.sudo.is
# legacy record :(
resource "digitalocean_record" "eyjabakki-sudo-is" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "A"
  name   = "eyjabakki"
  value  = "89.160.147.41"
  ttl    = 60
}

# # mathom.sudo.is
# resource "digitalocean_record" "mathom-sudo-is" {
#   domain = "${digitalocean_domain.sudo-is.name}"
#   type   = "A"
#   name   = "mathom"
#   value  = "89.17.135.222"
#   ttl    = 60
# }

# CNAME vpn.sudo.is
resource "digitalocean_record" "vpn-sudo-is" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "CNAME"
  name   = "vpn"
  value  = "${local.main_vpn}."
  ttl    = 60
}

# CNAME lychener-vpn.sudo.is
resource "digitalocean_record" "wifi001-vpn-sudo-is" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "CNAME"
  name   = "wifi001-vpn"
  value  = "lon-vpn.sudo.is."
  ttl    = 60
}

# CNAME nl-vpn.sudo.is
resource "digitalocean_record" "nl-vpn-sudo-is" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "CNAME"
  name   = "nl-vpn"
  value  = "dns0.lokun.is."
  ttl    = 60
}
