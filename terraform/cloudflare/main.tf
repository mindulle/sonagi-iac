data "cloudflare_zone" "sonagi_space" {
  name = "sonagi.space"
}

locals {
  zone_id    = data.cloudflare_zone.sonagi_space.id
  account_id = data.cloudflare_zone.sonagi_space.account_id
}

# Zero Trust Access Application 생성 (chat.sonagi.space 보호)
resource "cloudflare_zero_trust_access_application" "opencode_ui" {
  account_id                = local.account_id
  name                      = "Open Web UI"
  domain                    = "chat.sonagi.space"
  session_duration          = "730h"
  auto_redirect_to_identity = false
}

# Zero Trust Access Policy 생성 (특정 이메일만 허용)
resource "cloudflare_zero_trust_access_policy" "opencode_policy" {
  application_id = cloudflare_zero_trust_access_application.opencode_ui.id
  account_id     = local.account_id
  name           = "Allow Sonagi Dev"
  precedence     = "1"
  decision       = "allow"

  include {
    email = ["sonagi.dev@gmail.com"]
  }
}
