---
slug: argocd-gitops
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an ArgoCD GitOps config (Application / AppProject / ApplicationSet) with self-heal, sync-waves, and notifications enforcing Git as source of truth.
content_id: "76793d0b0e4227e3"
complexity: deep
produces: config
est_tokens: 4500
tags: [gitops, argocd, kubernetes, continuous-deployment]
---
# ArgoCD GitOps for Kubernetes Deployments

## Summary

**One-sentence:** Produces an ArgoCD GitOps config (Application / AppProject / ApplicationSet) with self-heal, sync-waves, and notifications enforcing Git as source of truth.

**One-paragraph:** ArgoCD implements GitOps for Kubernetes: Git is the single source of truth for cluster state, ArgoCD continuously reconciles live state toward the desired Git state. Use folders (not branches) to model environments. Use ApplicationSets to generate Applications across environments from a single template. Enable selfHeal to prevent configuration drift. Application manifests are themselves in Git (App-of-Apps or ApplicationSet); never created in the UI for production.

**Ефективно для:**

- Kubernetes workloads із GitOps-controlled deployments.
- multiple environments (dev/staging/prod) managed from single repository.
- multi-cluster management від central control plane.
- progressive delivery з Argo Rollouts (canary, blue-green).

## Applies If (ALL must hold)

- Workloads target a Kubernetes cluster managed by the team.
- Single Git repository can host environment manifests (overlays per env).
- Cluster can pull from the Git repo (network path + credentials configured).
- Team accepts Git as the source of truth — no manual `kubectl apply` in production.

## Skip If (ANY kills it)

- Non-Kubernetes deployments — ArgoCD only targets Kubernetes clusters.
- Single-developer project with simple `kubectl apply` — GitOps overhead is not justified.
- Workflows where the build artifact (Docker image) needs to be deployed immediately without a Git commit to update the image tag — requires a separate image-update automation step.
- Environments where Git access from the cluster is not possible (air-gapped without Git mirror).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Kubernetes cluster + kubeconfig | string + file | platform |
| Git repository for manifests | URL + credentials | platform |
| Environment overlays | folder structure | repo |
| Notification channel (Slack + ticketing) | webhook URLs | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/kubernetes-resources` | base Kubernetes resource shapes assumed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compose-application` | sonnet | Build Application / ApplicationSet manifest |
| `derive-appproject` | sonnet | Map team to sourceRepos / destinations / roles |
| `assign-sync-waves` | haiku | Mechanical numbering of resource dependencies |

## Templates

| File | Purpose |
|------|---------|
| `templates/application.yaml` | ArgoCD Application manifest skeleton |
| `templates/appproject.yaml` | AppProject with sourceRepos/destinations/roles |
| `templates/applicationset.yaml` | ApplicationSet generator across envs |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-argocd-gitops.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[kubernetes-resources]]
- [[helm-basics]]
- [[deploy-blue-green-canary]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the ArgoCD GitOps for Kubernetes Deployments methodology when in doubt about scope or fit.
