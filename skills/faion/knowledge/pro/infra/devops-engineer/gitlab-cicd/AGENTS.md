# GitLab CI/CD

## Summary

GitLab CI/CD is an integrated pipeline platform built into GitLab, configured via `.gitlab-ci.yml`. Pipelines are defined with stages, jobs, rules, and DAG dependencies (`needs:`). Use `rules:` (not deprecated `only/except`) for conditional execution and `needs:` for parallelization across stage boundaries.

## Why

GitLab CI/CD co-locates code, issues, registry, and pipelines — eliminating cross-tool authentication overhead. The DAG via `needs:` cuts wall-clock time by running jobs as soon as their specific dependencies complete, not after entire stages finish. Built-in security scan templates (SAST, DAST, container scanning) require zero external configuration.

## When To Use

- Project is hosted on GitLab (cloud or self-managed)
- Pipeline needs parent-child or dynamic child pipelines (monorepo)
- Team needs built-in container registry without external tooling
- GitLab-native environments and review apps are required
- Security scanning without external CI integration is needed

## When NOT To Use

- Repository is on GitHub — use GitHub Actions instead (native integration)
- Organization already invested in Jenkins with shared libraries — migration cost may exceed benefit
- Deployment target is exclusively managed by ArgoCD GitOps — push-based deploy conflicts with pull-based GitOps; trigger ArgoCD sync instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline-structure.xml` | Stage/job/DAG rules, caching vs artifact distinction, workflow rules, performance patterns |
| `content/02-security-deploy.xml` | Security scan templates, protected variables, environments, review apps, Docker build pattern |

## Templates

| File | Purpose |
|------|---------|
| `templates/build-node.yml` | Node.js build job template with cache and artifact |
| `templates/build-docker.yml` | Docker build/push using dind and BuildKit |
| `templates/deploy-k8s.yml` | Kubernetes rolling deploy via kubectl |
| `templates/deploy-helm.yml` | Helm upgrade/install deploy job |
| `templates/pipeline-full.yml` | Complete production pipeline example (Node.js + Docker + K8s) |
| `templates/prompt-generate.txt` | LLM prompt for generating a complete pipeline |
| `templates/prompt-optimize.txt` | LLM prompt for optimizing an existing pipeline |
