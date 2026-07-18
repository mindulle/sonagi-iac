# Spells Bot Core Credentials
variable "discord_token" {
  description = "Discord Bot Token"
  type        = string
  sensitive   = true
}

variable "discord_client_id" {
  description = "Discord Client ID"
  type        = string
}

# MinIO Credentials
variable "minio_access_key" {
  description = "MinIO Access Key"
  type        = string
  sensitive   = true
}

variable "minio_secret_key" {
  description = "MinIO Secret Key"
  type        = string
  sensitive   = true
}

# External API Tokens
variable "paperclip_api_token" {
  description = "Paperclip API Token"
  type        = string
  sensitive   = true
}

variable "notion_api_key" {
  description = "Notion API Key"
  type        = string
  sensitive   = true
}

variable "n8n_api_key" {
  description = "n8n API Key"
  type        = string
  sensitive   = true
}

# Centralized Webhooks
variable "webhook_alerts" {
  description = "Discord Webhook URL for System Alerts"
  type        = string
  sensitive   = true
  default     = ""
}

variable "webhook_accounting" {
  description = "Discord Webhook URL for Accounting/Ledger"
  type        = string
  sensitive   = true
  default     = ""
}
