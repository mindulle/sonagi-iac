# Sonagi IaC (Infrastructure as Code) Skill

이 스킬은 `sonagi-iac` (인프라스트럭처 자동화 및 배포) 프로젝트에서 작업하는 AI 에이전트를 위한 절대 지침입니다.

## 🤖 1. Agentic Coding Principles (Karpathy Rules)
1. **Think Before Coding**: 인프라 코드는 잘못 건드리면 전체 시스템 장애를 유발할 수 있습니다. 확신이 없다면 무조건 사용자에게 계획을 먼저 보고하고 승인을 받으십시오.
2. **Simplicity First**: 꼭 필요한 쿠버네티스 리소스나 앤서블 태스크만 작성하십시오. 미래를 대비한다는 이유로 불필요하게 복잡한 Helm Chart 템플릿이나 롤(Role) 분리를 하지 마십시오.
3. **Surgical Changes**: 요청받은 특정 서비스의 YAML 파일만 정밀하게 수정하십시오. 다른 서비스의 배포 매니페스트를 함부로 건드려서는 안 됩니다.
4. **Goal-Driven Execution**: 매니페스트를 수정할 때는 "이 매니페스트가 ArgoCD에 의해 배포되었을 때 파드가 정상적으로 뜨는지"를 목표로 삼고 코드를 작성하십시오.

## 🏛️ 2. Infrastructure & GitOps Rules
1. **ArgoCD (Kubernetes)**: 쿠버네티스 워크로드(Deployment, Service, Ingress 등)는 `kubernetes/` 디렉토리 하위의 각 서비스 폴더에 위치합니다. 배포는 ArgoCD를 통해 이루어지므로 `kubectl apply`를 명시적으로 지시하지 마십시오.
2. **Ansible (Node Provisioning)**: OCI 인스턴스 등 머신 자체의 프로비저닝이나 설정은 K3s 밖의 영역이며, 별도 저장소(`sonagi-iac-v3`)의 Ansible Playbook으로 관리됨을 인지하십시오.
3. **No Hardcoded Secrets**: 비밀번호, API 키, 토큰 등은 **절대** YAML 파일에 평문으로 커밋하지 마십시오. 반드시 `SealedSecret`을 사용하거나 주석 처리된 템플릿 형태로 제공하고 사용자에게 안내하십시오.
4. **Naming Convention**: 리소스 이름은 `[서비스명]-[리소스종류]` 형태를 유지하십시오. (예: `metabase-deployment`, `postgres-svc`)

## 🛠️ 3. Workflow
- 작업 시 반드시 새로운 브랜치를 따고 코드를 수정한 뒤, Pull Request(PR)를 올리십시오.
- PR 제목은 Conventional Commits (예: `feat: add redis deployment`)를 따르십시오.
