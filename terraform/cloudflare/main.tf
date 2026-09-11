data "cloudflare_zone" "sonagi_space" {
  name = "sonagi.space"
}

locals {
  zone_id    = data.cloudflare_zone.sonagi_space.id
  account_id = data.cloudflare_zone.sonagi_space.account_id
}


