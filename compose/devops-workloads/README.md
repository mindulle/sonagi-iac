# DevOps Workloads (Piston, PR-Agent, GitHub Runner)

이 디렉터리는 과거 `mindullemonitor` 노드의 k3s 클러스터에서 운영되던 3개 워크로드를 `devops` 노드의 경량 Docker Compose로 이관하여 운영하기 위한 SSOT 설정입니다.

## 포함된 서비스
1. **Piston (`:2000`)**: 다국어 코드 샌드박스 실행 엔진
2. **PR-Agent (`:3000`)**: GitHub PR 자동 리뷰 AI 웹훅 서비스
3. **GitHub Runner**: `llm-wiki` 전용 Docker 기반 Self-Hosted 액션 러너

## 배포 및 운영 가이드
1. 환경 설정 파일 복사:
   ```bash
   cp .env.pr-agent.example .env.pr-agent
   cp .env.github-runner.example .env.github-runner
   ```
2. Secret 파일 배치:
   - PR-Agent GitHub App Private Key (`pr-agent-private-key.pem`)
3. 기동:
   ```bash
   docker compose up -d
   ```
4. 헬스체크:
   - Piston: `curl http://localhost:2000/api/v2/runtimes`
   - PR-Agent: `curl http://localhost:3000/`
