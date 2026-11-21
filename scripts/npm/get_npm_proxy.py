"""NPM proxy host 하나의 업스트림 설정을 조회한다.

    export NPM_EMAIL='...'
    export NPM_PASSWORD='...'
    python3 get_npm_proxy.py [domain]

선택 환경변수: NPM_API_URL
"""

import os
import sys

import requests

API = os.environ.get("NPM_API_URL", "http://100.113.113.72:81/api")
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "npm.lab.sonagi.space"


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
    res = requests.get(
        f"{API}/nginx/proxy-hosts",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    res.raise_for_status()
    for host in res.json():
        if DOMAIN in host["domain_names"]:
            print(
                f"id={host['id']} domains={host['domain_names']} "
                f"-> {host['forward_scheme']}://{host['forward_host']}:{host['forward_port']} "
                f"enabled={host.get('enabled')}"
            )


if __name__ == "__main__":
    main()
