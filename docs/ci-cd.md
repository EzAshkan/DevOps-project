# CI/CD pipeline

The GitLab pipeline definition is [`.gitlab-ci.yml`](../.gitlab-ci.yml). It
uses the shared GitLab Runner described in [the Ansible Runner guide](../ansible/README.md).

## Pipeline flow

```text
test
├── backend_lint_test
└── frontend_lint_test
        ↓
build
├── build_backend_image  → backend-image.tar
└── build_frontend_image → frontend-image.tar
        ↓
publish
├── publish_backend_image  → Nexus hosted registry
└── publish_frontend_image → Nexus hosted registry
```

The test jobs use language-specific images: Python for Ruff and pytest, and
Node.js for npm, linting, and frontend tests. Image build and publish jobs use
the Docker CLI image because they run `docker build`, `docker save`, `docker
load`, and `docker push`.

The Runner provides Docker access through its configured Docker socket mount.
Only trusted team members should be able to modify pipeline code because that
access is powerful on the Runner host.

## Image artifact handoff

GitLab jobs are isolated, so a Docker image built in one job is not a reliable
input to a later job. The build jobs save the images as short-lived artifacts:

```bash
docker build --tag "$BACKEND_IMAGE" backend
docker save --output backend-image.tar "$BACKEND_IMAGE"
```

The corresponding publish job declares `needs` with `artifacts: true`, then
restores and pushes the same image:

```bash
docker load --input backend-image.tar
docker push "$BACKEND_IMAGE"
```

Artifact filenames must match exactly in `docker save`, `artifacts.paths`, and
`docker load`. The artifacts expire after one hour; they are only a CI handoff.
Nexus is the durable source from which Kubernetes and Argo CD will later pull
the deployable images.

## Nexus usage

The pipeline uses these non-secret configuration variables:

| Variable | Current endpoint | Purpose |
| --- | --- | --- |
| `NEXUS_DOCKERHUB_PROXY` | `nexus.server:8083` | Pull public tool and base images through the Docker Hub proxy. |
| `NEXUS_HOSTED_REGISTRY` | `nexus.server:8082` | Push TaskFlow images to the Docker Hosted repository. |
| `BACKEND_IMAGE` | `$NEXUS_HOSTED_REGISTRY/taskflow/backend:$CI_COMMIT_SHA` | Immutable backend image name. |
| `FRONTEND_IMAGE` | `$NEXUS_HOSTED_REGISTRY/taskflow/frontend:$CI_COMMIT_SHA` | Immutable frontend image name. |

The commit SHA tag is immutable for a particular pipeline. Do not use `latest`
as a deployment reference.

The current Nexus endpoints use HTTP for the lab environment. The Runner Docker
daemon must therefore be configured with the relevant Nexus endpoints as
insecure registries. Before production use, place Nexus behind TLS and remove
that exception.

## Secrets and publishing permissions

The following values are GitLab **CI/CD variables**, created in the GitLab UI;
they must never be committed to `.gitlab-ci.yml` or a `.env` file:

| Variable | Purpose |
| --- | --- |
| `NEXUS_USERNAME` | Dedicated least-privilege Nexus CI user, currently `taskflow-ci`. |
| `NEXUS_PASSWORD` | Password for that CI user. |

For a feature branch used during setup, variables need an `All (default)`
environment scope and must not be protected, otherwise GitLab does not inject
them into the job. Once the pipeline is stable, protect the variables and
allow automatic publishing only from trusted protected branches such as
`develop`.

## Planned improvements

1. Use `needs` so each backend/frontend build starts after its own test job,
   rather than waiting for every test job.
2. Cache pip and npm downloads to speed up repeat pipelines; keep Docker image
   archives as artifacts only.
3. Add Docker Buildx registry caching after the basic pipeline is stable.
4. Build multi-architecture images before deploying to mixed ARM64 and AMD64
   environments.
