### lokun.is
# A lokun.is
resource "digitalocean_domain" "lokun-is" {
  name = "lokun.is"
  ip_address = "${local.freespace_ip}"
}

# CNAME www.lokun.is
resource "digitalocean_record" "www-lokun-is" {
  domain = "${digitalocean_domain.lokun-is.name}"
  type   = "CNAME"
  name   = "www"
  value  = "${digitalocean_domain.lokun-is.name}."
  ttl    = 60
}

# api.lokun.is
resource "digitalocean_record" "api-lokun-is" {
  domain = "${digitalocean_domain.lokun-is.name}"
  type   = "A"
  name   = "api"
  value  = "178.79.148.123"
  ttl    = 60
}

# MX lokun.is
resource "digitalocean_record" "lokun-is-mx-0" {
  domain   = "${digitalocean_domain.lokun-is.name}"
  type     = "MX"
  name     = "@"
  priority = "10"
  value    = "ASPMX.L.GOOGLE.COM."
  ttl      = 60
}

# MX lokun.is
resource "digitalocean_record" "lokun-is-mx-1" {
  domain   = "${digitalocean_domain.lokun-is.name}"
  type     = "MX"
  name     = "@"
  priority = "20"
  value    = "ALT1.ASPMX.L.GOOGLE.COM."
  ttl      = 60
}

# MX lokun.is
resource "digitalocean_record" "lokun-is-mx-2" {
  domain   = "${digitalocean_domain.lokun-is.name}"
  type     = "MX"
  name     = "@"
  priority = "20"
  value    = "ALT2.ASPMX.L.GOOGLE.COM."
  ttl      = 60
}

# MX lokun.is
resource "digitalocean_record" "lokun-is-mx-3" {
  domain   = "${digitalocean_domain.lokun-is.name}"
  type     = "MX"
  name     = "@"
  priority = "30"
  value    = "ASPMX2.GOOGLEMAIL.COM."
  ttl      = 60
}

# MX lokun.is
resource "digitalocean_record" "lokun-is-mx-4" {
  domain   = "${digitalocean_domain.lokun-is.name}"
  type     = "MX"
  name     = "@"
  priority = "30"
  value    = "ASPMX3.GOOGLEMAIL.COM."
  ttl      = 60
}

# TXT lokun.is
resource "digitalocean_record" "lokun-is-txt" {
  domain = "${digitalocean_domain.lokun-is.name}"
  type   = "TXT"
  name   = "@"
  value  = "v=spf1 mx a ptr ptr:${digitalocean_domain.sudo-is.name} ip4:${local.freespace_ip}/32 include=_spf.investici.org"
  ttl    = 60
}

