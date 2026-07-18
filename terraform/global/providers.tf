terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }
}

provider "kubernetes" {
  # K3s 환경에 접근하기 위해 기본적으로 ~/.kube/config 를 참조합니다.
  # CI/CD 파이프라인이나 Atlantis 환경에서는 KUBE_CONFIG_PATH 환경 변수를 통해 주입할 수 있습니다.
  config_path = "~/.kube/config"
}
