# Server Configuration — Documentation

This document describes the `server-configuration.yml` Ansible playbook: what it does, why each part exists, how to run it, and a record of the successful run.

## Environment

- **Target OS**: Ubuntu (server)
- **Kubernetes**: minikube (single-node, `docker` driver) — chosen over a multi-node cluster for simplicity, since the project is a local/demo deployment
- **Control machine**: runs Ansible against the target server over SSH

## What the playbook does, section by section

### 1. Base OS setup
- Updates the apt cache and upgrades all packages (`dist` upgrade)
- Installs a set of base and quality-of-life packages:
  - Core: `curl`, `git`, `vim`, `htop`, `ca-certificates`, `gnupg`, `lsb-release`, `apt-transport-https`, `software-properties-common`, `conntrack`, `unzip`, `zip`
  - Handy tools (added later, per team request): `tree`, `ncdu`, `jq`, `net-tools`, `dnsutils`, `lsof`, `tmux`, `wget`, `bat`
  - Note: on Ubuntu, `bat` installs as the `batcat` binary (naming conflict with another package)

### 2. Team user accounts
Three accounts are created for the team: `MohammadReza`, `Zahra`, `Ashkan`.

- **Password login is disabled** (`password: "!"`) — accounts can only be accessed via SSH key
- Each user's SSH **public** key is installed via `ansible.posix.authorized_key`. Public keys were collected from each teammate directly.
- Each user is granted **sudo with password required** (not passwordless) — a deliberate tightening once SSH-key login was in place, since key-based login is a much stronger authentication story than password + `NOPASSWD` sudo
- Each user is added to the `docker` group so they can run Docker without `sudo`

**Requirement**: this task depends on the `ansible.posix` collection:
```bash
ansible-galaxy collection install ansible.posix
```

### 3. Docker Engine
Installed from Docker's **official** apt repository (not Ubuntu's default/outdated one):
- Adds Docker's GPG key and apt repo
- Installs `docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-buildx-plugin`, `docker-compose-plugin`
- Enables and starts the `docker` systemd service

### 4. kubectl
Downloaded directly as a binary from `dl.k8s.io` (pinned version, `kubectl_version` variable) to `/usr/local/bin/kubectl`.

### 5. minikube
Downloaded as a binary and started as a single-node cluster using the `docker` driver.

- **minikube_owner**: one designated user (initially `MohammadReza`, later changed to `Ashkan`) "owns" the cluster — its state lives entirely under that user's home directory (`~/.minikube`, `~/.kube`)
- The playbook checks if a cluster is already running (`minikube status`) before starting a new one, so re-runs are idempotent
- `become_user` + `become_flags: "-i"` + explicit `environment: HOME: ...` are used to ensure minikube runs correctly as the owner user (not root), with the right home directory and a proper login shell environment

### 6. Shared kubeconfig
Since only the owner has a real minikube cluster, the other team members need a way to run `kubectl` against it:
- The owner's kubeconfig (`~/.kube/config`) is copied to `/etc/shared-kube/config`
- That shared file is symlinked into every other user's `~/.kube/config`
- `KUBECONFIG=/etc/shared-kube/config` is exported for all users via `/etc/profile.d/kubeconfig.sh`

Result: all three team members can run `kubectl` commands against the same cluster; only the owner manages the cluster's lifecycle.

## How to run

### Prerequisites (on the control machine, not the target server)
```bash
# Install Ansible
sudo apt install ansible -y        # or: pip install ansible

# Install the required collection
ansible-galaxy collection install ansible.posix

# Install sshpass (needed for password-based auth with --ask-pass)
sudo apt install sshpass -y
```
Edit `inventory.ini`:
```ini
[devops_server]
server ansible_host=OUR_SERVER_IP ansible_user=root ansible_become=true
```
### First-time host key acceptance
```bash
ssh root@YOUR_SERVER_IP
exit
```

### Run
```bash
# Test connectivity
ansible -i inventory.ini devops_server -m ping

# Dry run (note: user-creation-dependent tasks like installing SSH keys
# will show expected errors in --check mode, since users don't really
# exist yet in a dry run — this is a known Ansible limitation, not a bug)
ansible-playbook -i inventory.ini server-configuration.yml --check

# Real run
ansible-playbook -i inventory.ini server-configuration.yml
```

### Verification after running
```bash
# Each teammate, from their own machine (using their own private key):
ssh <User>@OUR_SERVE_IP     # e.g. ssh Ashkan@...

docker ps
kubectl get nodes
```

## The successful full run — output log

The following is the console output from the first playbook run that completed with no failures (`ok=23 changed=0 unreachable=0 failed=0 skipped=1`). And one kubeconfig symlink task shows `skipping` for `Ashkan` (since the owner doesn't need a symlink to their own config).

```
PLAY [Configure DevOps server] ***********************************************

TASK [Gathering Facts] *********************************************************
[WARNING]: Host 'server' is using the discovered Python interpreter at
'/usr/bin/python3.12', but future installation of another Python interpreter
could cause a different interpreter to be discovered.
ok: [server]

TASK [Update apt cache] ********************************************************
ok: [server]

TASK [Upgrade all packages] ****************************************************
ok: [server]

TASK [Install base packages] ***************************************************
ok: [server]

TASK [Create team user accounts] ***********************************************
ok: [server] => (item=MohammadReza)
ok: [server] => (item=Zahra)
ok: [server] => (item=Ashkan)

TASK [Create .ssh directory for each user] *************************************
ok: [server] => (item=MohammadReza)
ok: [server] => (item=Zahra)
ok: [server] => (item=Ashkan)

TASK [Install each user's SSH public key] **************************************
ok: [server] => (item=MohammadReza)
ok: [server] => (item=Zahra)
ok: [server] => (item=Ashkan)

TASK [Grant team users sudo] ***************************************************
ok: [server] => (item=MohammadReza)
ok: [server] => (item=Zahra)
ok: [server] => (item=Ashkan)

TASK [Create keyrings directory] ***********************************************
ok: [server]

TASK [Add Docker GPG key] ******************************************************
ok: [server]

TASK [Add Docker apt repository] ***********************************************
ok: [server]

TASK [Install Docker Engine and plugins] ***************************************
ok: [server]

TASK [Ensure docker group exists] **********************************************
ok: [server]

TASK [Add team users to docker group] ******************************************
ok: [server] => (item=MohammadReza)
ok: [server] => (item=Zahra)
ok: [server] => (item=Ashkan)

TASK [Enable and start Docker service] *****************************************
ok: [server]

TASK [Download kubectl binary] *************************************************
ok: [server]

TASK [Download minikube binary] ************************************************
ok: [server]

TASK [Check if minikube cluster already exists for owner user] ****************
ok: [server]

TASK [Start minikube cluster (docker driver) as owner user] *******************
skipping: [server]

TASK [Create shared kube directory] ********************************************
ok: [server]

TASK [Copy owner's kubeconfig to shared location] ******************************
ok: [server]

TASK [Ensure .kube directories exist before symlinking] ************************
ok: [server] => (item=MohammadReza)
ok: [server] => (item=Zahra)
ok: [server] => (item=Ashkan)

TASK [Symlink shared kubeconfig into each user's home] *************************
ok: [server] => (item=MohammadReza)
ok: [server] => (item=Zahra)
skipping: [server] => (item=Ashkan)

TASK [Set KUBECONFIG env var for all users via profile.d] *********************
ok: [server]

PLAY RECAP **********************************************************************
server : ok=23  changed=0  unreachable=0  failed=0  skipped=1  rescued=0  ignored=0
```

## Open items / not yet enforced

- Only `minikube_owner` should run `minikube start/stop/delete` — currently a team convention, not technically restricted

