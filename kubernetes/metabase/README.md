# Metabase Deployment

K3s 클러스터 내부의 `bi` 네임스페이스에서 구동되는 Metabase(BI 도구) 매니페스트입니다.

## 🚀 아키텍처 특이사항 (PostgreSQL Backend)
- 멀티 노드 쿠버네티스 환경에서 파드가 다른 노드로 스케줄링되더라도 설정(대시보드)이 날아가지 않도록, 메타베이스의 Application Database를 로컬 SQLite(H2)에서 중앙 **PostgreSQL(`postgres-svc`)**로 이관했습니다.
- 따라서 메타베이스 파드는 완벽한 **Stateless** 상태로 동작하며 고가용성을 확보합니다.
- 단, `Eagle Gallery`나 `Notion` 등의 로컬 SQLite 연동을 위해 기존 PVC(`/metabase-data`) 마운트는 유지됩니다.

## ⚙️ 배포 전 필수 준비 작업
1. **PostgreSQL 데이터베이스 생성**:
   * `postgres-svc`에 접속하여 메타베이스를 위한 빈 데이터베이스를 하나 생성해야 합니다.
   ```sql
   CREATE DATABASE metabase_app;
   ```
2. **시크릿 생성**:
   * 생성한 DB에 접근할 계정 정보를 K3s에 주입합니다. (`05-secret-template.yaml` 참고)
   ```bash
   kubectl create secret generic metabase-db-secret \
     --namespace=bi \
     --from-literal=username="postgres계정" \
     --from-literal=password="postgres비밀번호"
   ```
3. 이후 ArgoCD를 통해 Sync를 맞추면 새로운 메타베이스가 구동됩니다.
