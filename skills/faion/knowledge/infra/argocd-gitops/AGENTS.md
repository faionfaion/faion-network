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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-argocd-gitops.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[helm-basics]]
- [[release-strategy-canary-blue-green-feature-flag]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the ArgoCD GitOps for Kubernetes Deployments methodology when in doubt about scope or fit.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/application.yaml`

```yaml
# ArgoCD GitOps for Kubernetes Deployments — application.yaml
# Replace placeholder values per instance.

artefact_id: "<slug-or-uuid>"
owner: "<single-named-handle>"
inputs_used: []
decision: "<the-answer>"
rationale: "<>=2 sentences referencing at least one input by name>"
version: "1.0.0"
last_reviewed: "2026-05-23"
```

### `templates/appproject.yaml`

```yaml
# ArgoCD GitOps for Kubernetes Deployments — appproject.yaml
# Replace placeholder values per instance.

artefact_id: "<slug-or-uuid>"
owner: "<single-named-handle>"
inputs_used: []
decision: "<the-answer>"
rationale: "<>=2 sentences referencing at least one input by name>"
version: "1.0.0"
last_reviewed: "2026-05-23"
```

### `templates/applicationset.yaml`

```yaml
# ArgoCD GitOps for Kubernetes Deployments — applicationset.yaml
# Replace placeholder values per instance.

artefact_id: "<slug-or-uuid>"
owner: "<single-named-handle>"
inputs_used: []
decision: "<the-answer>"
rationale: "<>=2 sentences referencing at least one input by name>"
version: "1.0.0"
last_reviewed: "2026-05-23"
```
