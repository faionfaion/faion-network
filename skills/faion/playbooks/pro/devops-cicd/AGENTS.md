# Pro / DevOps CI/CD Playbooks

GitHub Actions pipelines, deployment patterns, container builds, and release automation for agency teams. Citation scope: `knowledge/free/ + solo/ + pro/`.

## Playbooks

| Slug | Goal |
|------|------|
| `production-cicd-pipeline` | Multi-stage GitHub Actions pipeline: lint → test → scan → build → staging → gate → production |

## Authoring

Spec: `../../../../../.aidocs/conventions/playbooks/playbook-spec.md`. Validator: `python3 scripts/validate-tier-playbook.py <path>`.
