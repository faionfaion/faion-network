# ArgoCD GitOps

## Summary

ArgoCD is a declarative GitOps CD tool for Kubernetes (used in ~60% of K8s clusters per CNCF 2025). It synchronizes K8s cluster state from Git, detects drift, and enables automated or manual sync with rollback. Key rules: keep app code and GitOps config in separate repos; use folders for environments (not branches); always use Helm or Kustomize (never raw YAML); use ApplicationSets to automate multi-env or multi-cluster deployments. Never run `kubectl` directly in production — all changes must go through Git.

## Why

GitOps eliminates configuration drift by making Git the single source of truth and ArgoCD the enforcer. Any manual `kubectl apply` is automatically reverted (self-heal mode). The separate-repos rule prevents infinite CI trigger loops where a Git push to the app repo triggers CI which pushes to the same repo.

## When To Use

- Kubernetes-native deployments requiring automated sync and drift detection
- Multi-cluster deployments (ApplicationSet with Cluster generator)
- Teams adopting GitOps with PR-based change workflow for production
- Progressive delivery with canary or blue/green (via Argo Rollouts)
- Projects that need deployment audit trail via Git commit history

## When NOT To Use

- Non-Kubernetes workloads (VMs, serverless functions, legacy on-prem) — ArgoCD only manages K8s resources
- Single-developer projects with a single cluster — Helm + CI kubectl apply is simpler
- When the team is not ready to treat Git as the only truth — partial adoption breaks the model

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Core components, GitOps flow, anti-patterns table (raw YAML, kubectl in prod, branches for envs) |
| `content/02-rules.xml` | Separate repos rule, folder-over-branches rule, sync wave ordering, sync window for production |
| `content/03-applicationsets.xml` | List, Git directory, Pull Request, and Cluster generators with use cases |
| `content/04-examples.xml` | Application manifest, AppProject with RBAC, ApplicationSet for multi-env, sync hook patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/application.yaml` | ArgoCD Application with automated sync, self-heal, prune, and retry policy |
| `templates/appproject.yaml` | AppProject with source repo allowlist, destination namespace, and RBAC roles |
| `templates/applicationset-envs.yaml` | ApplicationSet using List generator for staging/production environments |
