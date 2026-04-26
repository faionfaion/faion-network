# GitOps

## Summary

GitOps uses a Git repository as the single source of truth for declarative infrastructure and applications. A pull-based operator (ArgoCD, FluxCD) running inside the cluster continuously reconciles live state with the desired state in Git, providing automatic drift detection and correction. The recommended pattern is hybrid: CI pipeline builds and pushes image tags / manifest updates to Git; the GitOps agent pulls and applies. Use folders (not branches) for environment separation.

## Why

Pull-based GitOps eliminates cluster credentials from CI pipelines, creates an immutable audit trail of every change, and enables automatic drift correction without manual intervention. 90%+ of Kubernetes deployments now use GitOps (2025 data); 80%+ of adopters report higher reliability. The audit trail satisfies compliance requirements that push-based pipelines cannot easily provide.

## When To Use

- Kubernetes-native deployments requiring drift detection and automatic reconciliation.
- Multi-cluster/multi-environment setups where consistency must be enforced.
- Compliance or audit requirements where every config change needs a Git trail.
- Progressive delivery (canary/blue-green) with automated metric-driven promotion.

## When NOT To Use

- Non-containerized legacy systems — GitOps tooling is Kubernetes-native.
- Teams with no Kubernetes experience — the learning curve adds cost before value.
- Tight deployment sequencing needs where push-based CI gives finer control.
- Small teams (<5 engineers) with a single environment and simple deploy pipeline.

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Core principles, push vs pull model comparison, repository structure patterns, environment strategy, tool comparison, progressive delivery |
| `content/02-checklist.xml` | Strategy selection, repository setup, ArgoCD/Flux installation, security (RBAC, secrets), sync policies, multi-cluster, monitoring, DR checklists |

## Templates

none
