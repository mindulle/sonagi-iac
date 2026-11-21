#!/bin/bash
# datamart 백업 신선도를 node_exporter textfile collector 형식으로 노출한다.
# cron: */5 * * * * /usr/local/bin/sonagi_backup_metrics.sh
set -euo pipefail

BACKUP_DIR="/mnt/monitoring/llmops_backup/warm_archive"
OUT_DIR="/var/lib/node_exporter/textfile"
OUT="${OUT_DIR}/sonagi_backup.prom"

mkdir -p "$OUT_DIR"

LATEST="$(ls -1t "$BACKUP_DIR"/datamart-*.sqlite 2>/dev/null | head -1 || true)"

{
  echo "# HELP sonagi_backup_last_success_timestamp_seconds Latest datamart backup mtime (unix seconds)"
  echo "# TYPE sonagi_backup_last_success_timestamp_seconds gauge"
  if [[ -n "${LATEST}" ]]; then
    ts="$(stat -c %Y "${LATEST}")"
    echo "sonagi_backup_last_success_timestamp_seconds ${ts}"
  else
    echo "sonagi_backup_last_success_timestamp_seconds 0"
  fi
} > "${OUT}.tmp"

mv "${OUT}.tmp" "${OUT}"
chmod 0644 "${OUT}"
