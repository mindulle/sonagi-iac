"""NPM에서 Let's Encrypt DNS-01 인증서를 발급하고 lab 호스트에 연결한다.

Cloudflare 토큰과 NPM 자격증명은 환경변수로만 받는다.

    export NPM_EMAIL='...'
    export NPM_PASSWORD='...'
    export CF_DNS_API_TOKEN='...'
    python3 issue_cert.py ["*.lab.sonagi.space,lab.sonagi.space"]

선택 환경변수: NPM_API_URL, CERT_PROPAGATION_SECONDS (기본 60)
"""

import os
import sys
import time

import requests

API = os.environ.get("NPM_API_URL", "http://100.113.113.72:81/api")
DOMAINS = (
    sys.argv[1] if len(sys.argv) > 1 else "*.lab.sonagi.space,lab.sonagi.space"
).split(",")
PROPAGATION = os.environ.get("CERT_PROPAGATION_SECONDS", "60")


def login() -> str:
    res = requests.post(
        f"{API}/tokens",
        json={
            "identity": os.environ["NPM_EMAIL"],
            "secret": os.environ["NPM_PASSWORD"],
        },
        timeout=15,
    )
    res.raise_for_status()
    return res.json()["token"]


def main() -> None:
    cf_token = os.environ["CF_DNS_API_TOKEN"]
    token = login()
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "provider": "letsencrypt",
        "domain_names": DOMAINS,
        "meta": {
            "dns_challenge": True,
            "dns_provider": "cloudflare",
            "dns_provider_credentials": f"# Cloudflare API token\ndns_cloudflare_api_token={cf_token}\n",
            "key_type": "ecdsa",
            "propagation_seconds": PROPAGATION,
        },
    }

    print("Requesting new certificate...")
    res = requests.post(
        f"{API}/nginx/certificates", json=data, headers=headers, timeout=30
    )
    if res.status_code not in (200, 201):
        raise SystemExit(f"Failed to request cert: {res.text}")

    cert_id = res.json()["id"]
    print(f"Certificate requested, ID: {cert_id}")

    host_fields = (
        "domain_names forward_host forward_port forward_scheme allow_websocket_upgrade "
        "block_exploits caching_enabled hsts_enabled hsts_subdomains http2_support meta "
        "locations advanced_config"
    ).split()

    for _ in range(12):
        time.sleep(10)
        status_res = requests.get(
            f"{API}/nginx/certificates/{cert_id}", headers=headers, timeout=15
        )
        status = status_res.json().get("status")
        print(f"Status: {status}")
        if status in ("ready", "provided"):
            break

    print("Updating hosts with new certificate...")
    hosts = requests.get(f"{API}/nginx/proxy-hosts", headers=headers, timeout=15).json()
    for host in hosts:
        if "lab.sonagi.space" not in str(host["domain_names"]):
            continue
        update = {field: host[field] for field in host_fields}
        update["certificate_id"] = cert_id
        update["ssl_forced"] = True
        if host.get("access_list_id"):
            update["access_list_id"] = host["access_list_id"]
        requests.put(
            f"{API}/nginx/proxy-hosts/{host['id']}",
            json=update,
            headers=headers,
            timeout=15,
        )
        print(f"Updated host {host['id']} with cert {cert_id}")

    print("All done!")


if __name__ == "__main__":
    main()
