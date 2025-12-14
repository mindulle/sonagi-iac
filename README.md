# Ansible Playbooks for Sonagi Infrastructure

Infrastructure automation playbooks for OCI instances.

## Playbooks

1. **system-update.yml** - Update and upgrade system packages
2. **docker-cleanup.yml** - Clean up unused Docker resources
3. **backup-services.yml** - Backup n8n, Semaphore, Atlantis
4. **log-rotation.yml** - Rotate and clean logs
5. **security-patch.yml** - Apply security updates

## Usage
```bash
# Update all systems
ansible-playbook -i inventory/hosts.ini playbooks/system-update.yml

# Docker cleanup
ansible-playbook -i inventory/hosts.ini playbooks/docker-cleanup.yml

# Backup all services
ansible-playbook -i inventory/hosts.ini playbooks/backup-services.yml
```

## Requirements

- Ansible 2.9+
- SSH access to all hosts
- Sudo privileges
