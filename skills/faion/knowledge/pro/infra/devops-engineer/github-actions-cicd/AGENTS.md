# GitHub Actions CI/CD

## Summary

GitHub Actions automates workflows defined in `.github/workflows/` YAML files, triggered by push, pull_request, schedule, and other events. The critical security rule: pin every third-party action to a full commit SHA, not a mutable tag. Always set explicit `permissions:` blocks at workflow or job level, defaulting to `contents: read`.

## Why

GitHub Actions is the native CI/CD for GitHub-hosted projects, eliminating webhook setup and credential management between CI and SCM. OIDC authentication (id-token: write) lets workflows authenticate to AWS/GCP/Azure without any stored long-lived secrets. Reusable workflows and composite actions eliminate copy-paste across repositories.

## When To Use

- Repository is hosted on GitHub
- Project needs matrix builds across OS/versions/runtimes
- Team wants OIDC-based credentialless cloud authentication
- Open source project needs free CI minutes
- Workflows must trigger on GitHub-native events (PR, release, issue)

## When NOT To Use

- Repository is on GitLab — use GitLab CI/CD instead
- Deployment is GitOps/ArgoCD-managed — trigger ArgoCD sync rather than kubectl in Actions
- Highly regulated environment requires runners on-prem and GitHub.com is not approved — self-hosted runners add operational burden; evaluate Jenkins or GitLab self-managed
- `pull_request_target` needed with untrusted fork code — high injection risk; use carefully

## Content

| File | What's inside |
|------|---------------|
| `content/01-security.xml` | Action pinning to SHA, GITHUB_TOKEN permissions, OIDC auth, checkout safety, injection prevention |
| `content/02-workflow-patterns.xml` | Concurrency groups, caching strategy, matrix builds, reusable workflows, composite actions, artifacts |

## Templates

| File | Purpose |
|------|---------|
| `templates/ci-node.yml` | Minimal Node.js CI (lint + test + build) |
| `templates/ci-python.yml` | Python CI with ruff/mypy and pytest coverage |
| `templates/docker-build.yml` | Multi-platform Docker build + GHCR push |
| `templates/reusable-deploy.yml` | Reusable workflow for environment deployments |
| `templates/composite-action.yml` | Composite action skeleton |
| `templates/prompt-generate.txt` | LLM prompt for generating a workflow |
| `templates/prompt-security-audit.txt` | LLM prompt for security-auditing a workflow |
