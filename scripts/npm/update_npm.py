"""모든 NPM proxy host에 `.lab.sonagi.space` 별칭 도메인을 추가한다.

    export NPM_EMAIL='...'
    export NPM_PASSWORD='...'
    python3 update_npm.py [--dry-run]

선택 환경변수: NPM_API_URL
"""

import os
import sys

import requests

API = os.environ.get("NPM_API_URL", "http://100.113.113.72:81/api")
DRY_RUN = "--dry-run" in sys.argv[1:]

FIELDS = (
    "forward_host forward_port forward_scheme allow_websocket_upgrade block_exploits "
    "caching_enabled certificate_id hsts_enabled hsts_subdomains http2_support meta "
    "locations advanced_config"
).split()


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
    token = login()
    headers = {"Authorization": f"Bearer {token}"}
    hosts = requests.get(f"{API}/nginx/proxy-hosts", headers=headers, timeout=15).json()

    for host in hosts:
        domains = host["domain_names"]
        new_domains = list(domains)
        for domain in domains:
            if domain.endswith(".sonagi.space") and not domain.endswith(
                ".lab.sonagi.space"
            ):
                alias = domain.replace(".sonagi.space", ".lab.sonagi.space")
                if alias not in new_domains:
                    new_domains.append(alias)

        if new_domains == domains:
            continue

        if DRY_RUN:
            print(f"[dry-run] {host['id']}: {domains} -> {new_domains}")
            continue

        update = {field: host[field] for field in FIELDS}
        update["domain_names"] = new_domains
        if host.get("access_list_id"):
            update["access_list_id"] = host["access_list_id"]

        res = requests.put(
            f"{API}/nginx/proxy-hosts/{host['id']}",
            json=update,
            headers=headers,
            timeout=15,
        )
        if res.status_code == 200:
            print(f"✅ Updated {host['id']}: {domains} -> {new_domains}")
        else:
            print(f"❌ Failed to update {host['id']}: {res.text}")

    print("Done!")


if __name__ == "__main__":
    main()
