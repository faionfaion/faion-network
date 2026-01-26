# GitOps

## Overview

GitOps is a set of practices that uses Git repositories as the single source of truth for declarative infrastructure and applications. Changes are made through Git commits and automatically applied to target environments through continuous reconciliation.

## When to Use

| Scenario | GitOps Fit |
|----------|-----------|
| Kubernetes-native deployments | Excellent |
| Multi-cluster/multi-environment | Excellent |
| Compliance/audit requirements | Excellent |
| Infrastructure as Code | Good |
| Teams requiring deployment visibility | Good |
| Non-containerized legacy systems | Limited |

## Core Principles (OpenGitOps)

| Principle | Description |
|-----------|-------------|
| Declarative | Infrastructure and applications defined as code in YAML/JSON |
| Versioned and Immutable | All configuration stored in Git with full history |
| Pulled Automatically | Agents pull changes from Git (not pushed by CI) |
| Continuously Reconciled | Automatic drift detection and correction |

## Push vs Pull Models (2025-2026)

### Pull-Based (Recommended)

GitOps operators (ArgoCD, FluxCD) running inside the cluster continuously pull changes from Git.

| Advantages | Disadvantages |
|------------|---------------|
| Better security (no external credentials) | Initial learning curve |
| Autonomous operation | Requires agent in each cluster |
| Automatic drift correction | Debugging can be complex |
| Multi-cluster native | |
| Audit trail built-in | |

**Best for:** Security-focused organizations, multi-cluster deployments, compliance requirements.

**Tools:** ArgoCD (60% K8s adoption 2025), Flux CD (CNCF graduated), Kargo.

### Push-Based

CI/CD pipelines push changes directly to environments after code changes.

| Advantages | Disadvantages |
|------------|---------------|
| Familiar CI/CD patterns | Credentials exposed outside cluster |
| Tight sequencing control | No automatic drift correction |
| Simpler initial setup | Manual reconciliation needed |
| Works with existing pipelines | Security audit complexity |

**Best for:** Teams with strong existing CI/CD, tight deployment sequencing needs.

**Tools:** GitHub Actions, GitLab CI, Jenkins, CircleCI.

### Hybrid Model (2025-2026 Trend)

Combines push for velocity with pull for safety.

```
CI Pipeline (Push)         GitOps Agent (Pull)
      |                           |
      v                           v
Build + Test              Continuous Reconciliation
      |                           |
      v                           v
Update manifests -----> Git Repo <----- Drift Detection
in Git                            |
                                  v
                           Auto-remediation
```

**Pattern:** CI pushes manifest updates to Git, GitOps agent pulls and applies.

## GitOps Flow

```
Developer     Git Repository     GitOps Agent     Kubernetes
    |               |                 |               |
    |-- commit ---->|                 |               |
    |               |<-- poll/watch --|               |
    |               |-- manifest ---->|               |
    |               |                 |-- apply ----->|
    |               |                 |<-- health ----|
    |               |                 |               |
    |               |     (continuous reconciliation) |
```

## Repository Structure Patterns

### Pattern 1: Monorepo (Recommended for <50 apps)

```
gitops-repo/
├── apps/
│   └── {app-name}/
│       ├── base/
│       │   ├── kustomization.yaml
│       │   ├── deployment.yaml
│       │   └── service.yaml
│       └── overlays/
│           ├── staging/
│           │   └── kustomization.yaml
│           └── production/
│               └── kustomization.yaml
├── infrastructure/
│   ├── cert-manager/
│   ├── ingress-nginx/
│   └── external-secrets/
├── clusters/
│   ├── staging/
│   └── production/
└── projects/
    └── team-*.yaml
```

### Pattern 2: Multi-Repo (Large organizations)

```
{org}/
├── gitops-apps-{team}/        # Team-owned app configs
├── gitops-infrastructure/      # Platform team owned
├── gitops-clusters/           # Cluster bootstrapping
└── gitops-projects/           # RBAC and projects
```

### Environment Strategy

| Strategy | When to Use |
|----------|-------------|
| Folders (recommended) | Most cases - clear separation |
| Branches | Strict promotion gates needed |
| Tags | Immutable environment snapshots |

**Best Practice:** Use folders, not branches for environments.

## Tools Comparison (2025-2026)

| Tool | Type | Best For | Adoption |
|------|------|----------|----------|
| ArgoCD | Pull | Web UI, multi-cluster (100+), RBAC/SSO | 60% K8s |
| Flux CD | Pull | Lightweight, multi-source, modular | CNCF graduated |
| Kargo | Pull | Multi-env promotion (staging->prod) | Emerging |
| Flagger | Pull | Automated canary/blue-green | Progressive |
| GitHub Actions | Push | CI-heavy workflows | High |
| GitLab CI | Hybrid | Native Flux integration | Growing |

## Progressive Delivery (2025-2026)

### Canary Deployments

```
v1 (stable) -----> 90% traffic
                      |
v2 (canary) -----> 10% traffic
                      |
           Analysis (Prometheus metrics)
                      |
         Success? ---> Promote to 100%
         Failure? ---> Rollback automatically
```

### Blue-Green Deployments

```
Blue (current) <--- Production traffic
Green (new)    <--- Test traffic only
                      |
           Validation passed?
                      |
Switch traffic -----> Green becomes Blue
Old Blue -------> Terminate
```

### Tools for Progressive Delivery

| Tool | Strategy | Integration |
|------|----------|-------------|
| Argo Rollouts | Canary, Blue-Green | ArgoCD native |
| Flagger | Canary, A/B, Blue-Green | Flux native |
| Istio | Traffic splitting | Service mesh |
| Linkerd | Traffic splitting | Service mesh |

## AI-Assisted GitOps (2025-2026)

Emerging capabilities:

- **Akuity AI (Sept 2025):** Auto-rollback on deployment failures
- **Flux AI experiments:** AI-assisted workflows via operator ecosystem
- **Spacelift Intent:** Natural language infrastructure provisioning
- **Drift analysis:** AI-powered root cause analysis

## Stats (2025-2026)

| Metric | Value |
|--------|-------|
| K8s deployments using GitOps | 90%+ |
| Organizations planning to continue/increase GitOps | 93% |
| Adopters reporting higher reliability | 80%+ |
| ArgoCD K8s cluster adoption | 60% |
| Organizations adopted by mid-2025 | Two-thirds |

## Folder Contents

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts |
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Complete code examples |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for GitOps tasks |

## Related Tools

| Tool | Purpose |
|------|---------|
| [ArgoCD](../argocd-gitops/) | Pull-based GitOps for Kubernetes |
| [GitHub Actions](../github-actions-cicd/) | CI/CD pipelines |
| [Kubernetes](../kubernetes/) | Container orchestration |
| [Helm](../helm-charts/) | Package management |

## References

- [OpenGitOps Principles](https://opengitops.dev/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Flux CD Documentation](https://fluxcd.io/docs/)
- [CNCF GitOps Working Group](https://github.com/open-gitops/documents)
- [GitOps in 2025 - CNCF](https://www.cncf.io/blog/2025/06/09/gitops-in-2025-from-old-school-updates-to-the-modern-way/)
- [Push vs Pull GitOps - Aviator](https://www.aviator.co/blog/choosing-between-pull-vs-push-based-gitops/)
- [Top GitOps Tools 2026 - Spacelift](https://spacelift.io/blog/gitops-tools)
