# ArgoCD GitOps

## Summary

ArgoCD implements GitOps for Kubernetes: Git is the single source of truth for cluster state, ArgoCD continuously reconciles live state toward the desired Git state. Use folders (not branches) to model environments. Use ApplicationSets to generate Applications across environments from a single template. Enable `selfHeal: true` to prevent configuration drift.

## Why

Push-based deployment (CI applies kubectl/helm) means the CI system needs cluster credentials and any out-of-band change goes undetected. ArgoCD's pull-based model eliminates CI-to-cluster credential exposure, provides real-time drift detection, and makes rollback an atomic Git revert rather than a re-deployment sequence.

## When To Use

- Kubernetes workloads that need GitOps-controlled deployments
- Multiple environments (dev/staging/prod) managed from a single repository
- Multi-cluster management from a central control plane
- Progressive delivery with Argo Rollouts (canary, blue-green)
- Teams that require deployment audit trail via Git history

## When NOT To Use

- Non-Kubernetes deployments — ArgoCD only targets Kubernetes clusters
- Single-developer project with simple `kubectl apply` — GitOps overhead is not justified
- Workflows where the build artifact (Docker image) needs to be deployed immediately without a Git commit to update the image tag — requires a separate image-update automation step (Argo CD Image Updater or CI commit)
- Environments where Git access from the cluster is not possible (air-gapped without Git mirror)

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Application, Project, ApplicationSet, sync strategies, hub-spoke vs distributed architecture |
| `content/02-configuration.xml` | Repository structure (base/overlay), RBAC via Projects, sync waves, hooks, notifications, sync windows |

## Templates

| File | Purpose |
|------|---------|
| `templates/application.yaml` | ArgoCD Application manifest with auto-sync and self-heal |
| `templates/applicationset-matrix.yaml` | ApplicationSet matrix generator for multi-env multi-cluster |
| `templates/appproject.yaml` | AppProject with RBAC scoping for a team |
| `templates/prompt-setup.txt` | LLM prompt for generating ArgoCD configuration |
