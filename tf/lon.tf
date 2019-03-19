resource "digitalocean_droplet" "lon-vpn" {
  image  = "ubuntu-18-04-x64"
  region = "lon1"
  size   = "512mb"
  name   = "lon-vpn.${digitalocean_domain.sudo-is.name}"
  ssh_keys = ["cb:79:d0:73:55:b1:79:60:a4:a9:d5:48:53:e2:67:13"]

  # A remote-exec wait untils the instance is ready
  # (also, we need python for ansible)
  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sleep 3",
      "sudo apt-get install -y python"
    ]
  }

  # provisioner "local-exec" {
  #   command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -u root -i '${self.ipv4_address},' ../ansible/lon-vpn.yml"
  # }

  private_networking = true

}

output "lon-vpn" {
  value = "${digitalocean_droplet.lon-vpn.ipv4_address}"
}

resource "digitalocean_record" "lon-vpn" {
  domain = "${digitalocean_domain.sudo-is.name}"
  type   = "A"
  name   = "lon-vpn"
  value  = "${digitalocean_droplet.lon-vpn.ipv4_address}"
  ttl    = 60
}
