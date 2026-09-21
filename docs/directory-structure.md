# Directory structure

## Purpose

The original source layout used `source code/` with `Back` and `Front`. It was reorganized to remove spaces and make paths predictable for future Docker, CI/CD, Ansible, Helm, and Kubernetes work.

## Change record

| Original path | New path | Reason |
| --- | --- | --- |
| `source code/Back/` | `backend/` | Clear backend component boundary and shell-safe path. |
| `source code/Front/` | `frontend/` | Clear frontend component boundary and shell-safe path. |
| `requirements.txt` | `backend/requirements.txt` | Keep Python dependencies next to the backend that uses them. |
| `Final_Project_DevOps2.pdf` | `docs/project-brief.pdf` | Preserve the assignment brief as project documentation. |

## Current layout

```text
.
├── backend/       # FastAPI source, tests, and requirements.txt
├── frontend/      # React/Vite source
├── docs/          # Team and project documentation
├── ansible/       # Future Ubuntu provisioning
├── helm/          # Future Helm chart
├── k8s/           # Future raw Kubernetes manifests
├── .env.example   # Local configuration reference; no secrets
└── README.md
```

The package name inside `backend/` remains `Back`. This branch changes paths only; it does not rename Python modules or change application behavior.
