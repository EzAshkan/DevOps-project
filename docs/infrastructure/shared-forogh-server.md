# Forogh Shared DevOps Server

## Purpose

This server is the shared team environment for the Kubernetes learning and integration phases. It will host the Minikube development cluster after the local Docker and CI/CD phases are stable.

## Provider and configuration

| Item | Value |
| --- | --- |
| Logical name | `forogh-shared-devops-server` |
| Provider | Forogh |
| Operating system | Ubuntu 24.04 LTS |
| CPU | 4 vCPU |
| Memory | 12 GB RAM |
| Storage | 75 GB SSD |

## Planned workloads

- Minikube development cluster
- TaskFlow application workloads
- Traefik ingress controller
- Argo CD
- Prometheus monitoring
- HPA and VPA demonstrations
- Rancher, only after the mandatory components are stable

## Access and security rules

- Each teammate uses an individual SSH key and account.
- SSH keys are allowed; passwords and private keys are never committed to Git.
- Do not document the server IP address, credentials, or kubeconfig contents in this repository.
- The Kubernetes API and management dashboards must not be exposed publicly without authentication and TLS.

## Capacity note

This configuration is suitable for a shared learning and demonstration environment. It is a single-server deployment, so it does not provide true infrastructure high availability. Resource usage must be monitored before installing optional tools together.
