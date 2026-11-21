# legacy/k8s

2026-10-31에 k3s가 비활성화되고, 2026-11-21에 devops에서 완전히 제거되었습니다.
이 디렉터리의 Ansible 자산은 **당시 k3s 클러스터용**이며 현재는 실행 대상이 없습니다.

| 자산 | 원래 역할 | 현재 대체 |
| --- | --- | --- |
| `ansible/playbooks/deploy-minio.yml`, `ansible/roles/minio/` | MinIO를 k8s 매니페스트로 배포 | devops의 docker 컨테이너(`minio`) |
| `deploy_jupyterhub.yml`, `roles/jupyterhub/` | JupyterHub를 Helm으로 배포 | 미사용 (재도입 시 재작성 필요) |

참고용으로만 보존합니다. 다시 쓰려면 k3s/Helm 환경을 먼저 복구해야 합니다.
