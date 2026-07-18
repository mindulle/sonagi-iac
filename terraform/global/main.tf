# Spells-bot 인증 정보와 중앙화된 Webhook 주소들을 담는 K3s Secret
resource "kubernetes_secret" "spells_bot_credentials" {
  metadata {
    name      = "spells-bot-credentials"
    namespace = "default"
  }

  type = "Opaque"

  data = {
    "DISCORD_TOKEN"       = var.discord_token
    "DISCORD_CLIENT_ID"   = var.discord_client_id
    "MINIO_ACCESS_KEY"    = var.minio_access_key
    "MINIO_SECRET_KEY"    = var.minio_secret_key
    "PAPERCLIP_API_TOKEN" = var.paperclip_api_token
    "NOTION_API_KEY"      = var.notion_api_key
    "N8N_API_KEY"         = var.n8n_api_key

    # 중앙 집중형 웹훅 관리 (n8n 및 스크립트에서 참조 예정)
    "WEBHOOK_ALERTS"     = var.webhook_alerts
    "WEBHOOK_ACCOUNTING" = var.webhook_accounting
  }
}
