# GitHub Self-Hosted Runner (K3s)

내부망(K3s)에서 구동되며 `postgres-svc` 등 클러스터 내부 자원에 직접 접근할 수 있는 GitHub Actions Runner입니다.

## 🚀 설정 및 배포 방법

1. **러너 토큰 발급**:
   * `llm-wiki` 레포지토리 이동 -> `Settings` -> `Actions` -> `Runners` -> `New self-hosted runner`
   * 화면에 표시되는 `Configure` 섹션에서 임시 토큰(Token) 복사
2. **시크릿 생성**:
   * 복사한 토큰을 사용하여 Kubernetes 클러스터에 Secret을 직접 생성합니다.
   ```bash
   kubectl create secret generic github-runner-secret \
     --namespace=bi \
     --from-literal=token="여기에_복사한_토큰_입력"
   ```
3. **ArgoCD Sync (또는 kubectl apply)**:
   * 이 폴더의 `01-deployment.yaml`이 ArgoCD를 통해 배포되면, 컨테이너가 기동되면서 자동으로 GitHub에 러너를 등록합니다.
   * `llm-wiki`의 워크플로우 파일(`sync-wiki-db.yml`)에서 `runs-on: ubuntu-latest`를 `runs-on: [self-hosted, internal-db]`로 변경하면 끝입니다!
