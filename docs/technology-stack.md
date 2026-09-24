# Technology stack

| Area | Technology | Current or planned role |
| --- | --- | --- |
| Backend | Python, FastAPI, SQLAlchemy | HTTP API and persistence access. |
| Frontend | React 18, Vite, plain CSS | Browser user interface. |
| Database | PostgreSQL | Task and user data storage. |
| Cache | Redis | Optional cache support. |
| Shared server | Forogh provider, Ubuntu 24.04 | Planned shared environment for Minikube and team integration work. |
| Local orchestration | Docker Compose | Planned local stack. |
| CI/CD | GitLab CI/CD | Backend/frontend lint and test jobs; Docker image build and publish stages are configured. |
| Image registry | Shared Nexus | Docker Hub proxy for public images and Docker Hosted repository for TaskFlow images. |
| Orchestration | Kubernetes / Minikube | Planned shared development cluster. |
| Packaging | Helm | Planned Kubernetes application packaging. |
| GitOps | Argo CD | Planned Git-driven deployment reconciliation. |
| Provisioning | Ansible | Planned Ubuntu machine setup. |
| Ingress | Traefik | Planned HTTP/HTTPS entry point. |
| Cluster management | Rancher | Planned cluster-management UI. |
| Monitoring | Prometheus | Planned metrics collection. |
