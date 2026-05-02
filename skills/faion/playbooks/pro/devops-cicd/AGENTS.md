# Pro / DevOps CI/CD Playbooks

GitHub Actions pipelines, deployment patterns, container builds, and release automation for agency teams. Citation scope: `knowledge/free/ + solo/ + pro/`.

## Playbooks

| Slug | Goal |
|------|------|
| `production-cicd-pipeline` | Multi-stage GitHub Actions pipeline: lint → test → scan → build → staging → gate → production |
| `deploy-blue-green-canary` | Zero-downtime blue/green ECS+ALB cutover (10 s) and canary 5%→25%→100% weighted routing with rollback |

## Authoring

Spec: `../../../../../.aidocs/conventions/playbooks/playbook-spec.md`. Validator: `python3 scripts/validate-tier-playbook.py <path>`.
