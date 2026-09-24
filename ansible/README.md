# Ansible automation

This directory contains the playbooks used to manage shared project infrastructure.

## Shared GitLab Runner

`playbooks/gitlab-runner.yml` installs and maintains one GitLab Runner container on the shared server. The Runner uses the Docker executor and is shared through GitLab project permissions; teammates do not need server access to run CI jobs.

The `gitlab_runner` role:

1. Creates the Runner Compose directory.
2. Renders `compose.yml` from a template.
3. Starts the container when its configuration changes or it is stopped.
4. Verifies that the Runner is running.

Runner configuration persists in the Docker volume `gitlab-runner-config`. The Compose definition is stored in `/home/<remote-user>/gitlab-runner/`.

### Prerequisites

- Ansible is installed on the local control machine.
- The remote `ansible_user` can connect with an SSH key and can run Docker without `sudo`.
- Docker Engine and Docker Compose are installed on the target server.

### Inventory

Copy the example inventory locally and fill in your own server details:

```bash
cp inventory/devops-server.ini.example inventory/devops-server.ini
```

`inventory/devops-server.ini` is ignored by Git. Never commit a real server IP, private-key path, SSH key, password, or GitLab Runner authentication token.

### Run

Run commands from this directory:

```bash
ansible-playbook -i inventory/devops-server.ini \
  --syntax-check playbooks/gitlab-runner.yml

ansible-playbook -i inventory/devops-server.ini \
  playbooks/gitlab-runner.yml
```

Registration is intentionally a separate, manual step because the GitLab Runner authentication token must not be stored in Git:

```bash
docker exec -it gitlab-runner gitlab-runner register
docker exec gitlab-runner gitlab-runner verify
```

## Security note

The Runner mounts `/var/run/docker.sock` so Docker-executor CI jobs can build images. Docker-socket access is highly privileged; use this Runner only for trusted project code and do not expose registration tokens or Docker credentials in the repository.
