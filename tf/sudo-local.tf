### sudo.local
resource "digitalocean_domain" "sudo-local" {
  name       = "sudo.local"
  ip_address = "127.0.0.1"
}

