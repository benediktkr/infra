variable "do_token" {}

variable "cf_token" {}
variable "cf_email" {}

provider "digitalocean" {
  token = var.do_token
}

provider "cloudflare" {
  email     = var.cf_email
  api_key = var.cf_token
}
