# Team workflow

## Branches

| Branch | Purpose |
| --- | --- |
| `main` | Stable, demo-ready code only. |
| `develop` | Shared integration branch. |
| `feature/*` | One focused change, created from `develop`. |

## Change flow

1. Update the local `develop` branch.
2. Create one focused `feature/*` branch.
3. Make and test the change locally.
4. Push the branch and open a merge request into `develop`.
5. A teammate reviews the merge request.
6. Merge only after required checks pass.
7. Merge `develop` into `main` only when the milestone is demo-ready.

## Working agreements

- Do not commit `.env`, tokens, kubeconfigs, passwords, or generated dependency directories.
- Keep one concern per merge request; do not mix Docker, CI/CD, and Helm work in one change.
- Update the relevant document when a structural or operational decision changes.
- Use commit-SHA image tags in later CI/CD stages; do not deploy `latest`.
