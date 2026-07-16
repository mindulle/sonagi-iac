terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

provider "cloudflare" {
  # API Token은 보안을 위해 환경변수(CLOUDFLARE_API_TOKEN)로 주입받습니다.
}
