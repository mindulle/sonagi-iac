"""NPM(nginx-proxy-manager) 인증서 만료 확인.

자격증명은 저장소에 두지 않고 환경변수로 받는다.

    export NPM_EMAIL='...'
    export NPM_PASSWORD='...'
    python3 check_cert.py [cert_id]

선택 환경변수: NPM_API_URL (기본 http://100.113.113.72:81/api)
"""

import os
import sys

import requests

API = os.environ.get("NPM_API_URL", "http://100.113.113.72:81/api")
CERT_ID = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("NPM_CERT_ID", "8")


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
        f"{API}/nginx/certificates/{CERT_ID}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    res.raise_for_status()
    cert = res.json()
    print("Expires:", cert.get("expires_on"))
    print("Domains:", cert.get("domain_names"))


if __name__ == "__main__":
    main()
