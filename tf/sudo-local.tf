### sudo.local
resource "digitalocean_domain" "sudo-local" {
  name = "sudo.local"
  ip_address = "127.0.0.1"
}

resource "digitalocean_domain" "ms" {
  name = "care.com"
  ip_address = "12.34.56.87"
}
