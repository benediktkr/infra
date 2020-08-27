variable "do_token" {}

variable "cf_token_custom" {}
variable "cf_token_general" {}
variable "cf_email" {}

provider "digitalocean" {
  token = var.do_token
}

provider "cloudflare" {
  email      = var.cf_email
  api_token  = var.cf_token_custom
 #api_key    = var.cf_token_general
}
