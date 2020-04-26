### sudo.is
resource "digitalocean_domain" "sudo-is" {
  name = "sudo.is"
  ip_address = "${local.f_ip}"
}

# MX sudo.is
resource "digitalocean_record" "sudo-is-mx-0" {
  domain   = "${digitalocean_domain.sudo-is.name}"
  type     = "MX"
  name     = "@"
  priority = "10"
  value    = "in1-smtp.messagingengine.com."
  ttl      = 60
}

# MX sudo.is
resource "digitalocean_record" "sudo-is-mx-1" {
  domain   = "${digitalocean_domain.sudo-is.name}"
  type     = "MX"
  name     = "@"
  priority = "20"
  value    = "in2-smtp.messagingengine.com."
  ttl      = 60
}


# DKIM records
resource "digitalocean_record" "dkim-1" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "CNAME"
  name   = "fm1._domainkey"
  value  = "fm1.sudo.is.dkim.fmhosted.com."
  ttl    = 43200
}
resource "digitalocean_record" "dkim-2" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "CNAME"
  name   = "fm2._domainkey"
  value  = "fm2.sudo.is.dkim.fmhosted.com."
  ttl    = 43200
}
resource "digitalocean_record" "dkim-3" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "CNAME"
  name   = "fm3._domainkey"
  value  = "fm3.sudo.is.dkim.fmhosted.com."
  ttl    = 43200
}

# TXT
resource "digitalocean_record" "sudo-is-txt" {
  domain   = "${digitalocean_domain.sudo-is.name}"
  type   = "TXT"
  name   = "@"
  value  = "v=spf1 mx a ptr ip4:176.9.152.42/32 ip4:176.9.53.236 include=_spf.investici.org include:spf.messagingengine.com ?all"
  ttl    = 60
}

resource "digitalocean_record" "sudo-is-google-txt" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "TXT"
  name   = "@"
  value  = "google-site-verification=anu1tuByz3JmonTIET79s6uokfXMvqi8tdemUsS1EWI"
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

# CNAMEs to f
locals {
  f_cnames = [
    "benedikt",
    "static",
    "notes",
    "nextcloud",
    "de-vpn"
  ]
}

resource "digitalocean_record" "f-cnames" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "CNAME"
  name   = "${element(local.f_cnames, count.index)}"
  count  = "${length(local.f_cnames)}"
  value  = "f.sudo.is."
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

# mathom.sudo.is
resource "digitalocean_record" "mathom-sudo-is" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "A"
  name   = "mathom"
  value  = "89.17.144.78"
  ttl    = 60
}

# CNAME vpn.sudo.is
resource "digitalocean_record" "vpn-sudo-is" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "CNAME"
  name   = "vpn"
  value  = "${local.main_vpn}."
  ttl    = 60
}

# CNAME wifi001-vpn.sudo.is
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
  value  = "dns0.sudo.is."
  ttl    = 60
}

# CNAME pi0.sudo.is (via afraid.org)
resource "digitalocean_record" "pi0-sudo-is" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "CNAME"
  name   = "pi0"
  value  = "pi0.strangled.net."
  ttl    = 60
}

# CNAME hh19.sudo.is (via afraid.org)
resource "digitalocean_record" "l54-sudo-is" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "CNAME"
  name   = "l54"
  value  = "pi0.strangled.net."
  ttl    = 60
}
