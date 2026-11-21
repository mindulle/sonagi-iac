# NPM 운영 스크립트

Nginx Proxy Manager(`http://100.113.113.72:81`)를 API로 다루는 일회성 도구 모음입니다.
**자격증명은 저장소에 두지 않습니다.** 실행 전에 환경변수로 주입하세요.

```bash
export NPM_API_URL='http://100.113.113.72:81/api'   # 선택
export NPM_EMAIL='...'
export NPM_PASSWORD='...'
export CF_DNS_API_TOKEN='...'   # issue_cert.py 에서만 필요
```

로컬에 저장된 자격증명을 쓰려면(2026-11-21 회전본):

```bash
set -a; . ~/.secrets/npm-admin; set +a
```

| 스크립트 | 용도 |
| --- | --- |
| `check_cert.py [cert_id]` | 인증서 만료일·도메인 확인 |
| `get_npm_proxy.py [domain]` | 프록시 호스트 업스트림 조회 |
| `update_npm.py [--dry-run]` | `.lab.sonagi.space` 별칭 도메인 일괄 추가 |
| `issue_cert.py [domains]` | Let's Encrypt DNS-01(Cloudflare) 인증서 발급 후 lab 호스트에 연결 |

## 주의

- `issue_cert.py`는 Cloudflare DNS 편집 권한 토큰이 필요합니다. 인증서 자동 갱신(renewal)도 같은 토큰을 쓰므로 **폐기 전에 대체 토큰을 먼저 발급**하세요.
- NPM API를 직접 호출하면 UI 없이도 프록시 설정이 바뀝니다. `--dry-run`이 있는 스크립트는 먼저 그것으로 확인하세요.
