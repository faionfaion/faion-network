---
id: gitops
name: "GitOps"
domain: OPS
skill: faion-cicd-engineer
category: "best-practices-2026"
---

# GitOps

## Problem

Manual deployments cause inconsistency, configuration drift, and unreliable releases.

## Solution: Git as Single Source of Truth

GitOps is a set of practices that uses Git repositories as the single source of truth for declarative infrastructure and applications.

## Core Principles (OpenGitOps)

| Principle | Description |
|-----------|-------------|
| **Declarative** | Infrastructure described in YAML/HCL, not imperative scripts |
| **Versioned** | All config in Git with complete history and audit trail |
| **Pulled Automatically** | Agents pull from Git, not pushed by CI |
| **Continuously Reconciled** | Automatic drift detection and self-healing |

## Push vs Pull Models

| Model | Description | Best For |
|-------|-------------|----------|
| **Pull-based** | GitOps operator in cluster polls Git for changes | Security, multi-cluster, self-healing |
| **Push-based** | CI/CD pipeline pushes changes to cluster | Tight control, sequencing, existing pipelines |
| **Hybrid (2025-2026)** | Push for velocity, pull for safety and drift correction | Enterprise environments needing both |

### Pull-Based Advantages

- Egress-only connections (no cluster exposure)
- No credentials distributed to external services
- Self-healing drift correction
- Better compliance and auditability

### Push-Based Advantages

- Works with existing CI/CD pipelines
- Better for non-Kubernetes environments
- Simpler initial setup
- Tight deployment sequencing control

## GitOps Workflow

```
Developer commits → Git Repository
        ↓
    Pull Request → Review & Approve
        ↓
    Merge to main
        ↓
GitOps Operator detects change (ArgoCD/Flux)
        ↓
    Applies to cluster
        ↓
Continuous reconciliation (drift correction)
```

## Tools Comparison (2025-2026)

| Tool | Type | Strengths | Considerations |
|------|------|-----------|----------------|
| **ArgoCD** | Pull | Web UI, multi-cluster (100+), RBAC with SSO, strong ecosystem | Heavier resource footprint |
| **Flux** | Pull | Lightweight, modular, multi-source, native K8s | No built-in UI, Weaveworks shutdown (2024) |
| **Kargo** | Promotion | Multi-environment promotion (staging → prod) | Akuity ecosystem |
| **Flagger** | Delivery | Automated canary, progressive delivery | Works with ArgoCD/Flux |
| **Spinnaker** | Multi-cloud | Advanced deployment strategies, multi-cloud | Complex setup |

### ArgoCD vs Flux Decision Matrix

| Factor | ArgoCD | Flux |
|--------|--------|------|
| UI/UX | Built-in web UI | CLI-first, external UI options |
| Learning curve | Lower | Higher |
| Resource usage | Higher | Lower |
| Multi-tenancy | Good | Excellent |
| Commercial support | Strong (Akuity, others) | CNCF community |
| Market share (2025) | ~60% | ~25% |
| Best for | Teams, visibility, onboarding | Platform engineers, automation |

**2025-2026 Recommendation:** ArgoCD for most teams (especially new to GitOps). Flux for platform engineers building automation or with existing Flux deployments.

## Repository Structure

### Recommended: Monorepo with Folders per Environment

```
gitops-repo/
├── base/                    # Shared configurations
│   ├── namespace.yaml
│   └── common-resources/
├── clusters/
│   ├── production/
│   │   ├── kustomization.yaml
│   │   └── apps/
│   └── staging/
│       ├── kustomization.yaml
│       └── apps/
├── infrastructure/
│   ├── base/
│   ├── production/
│   └── staging/
└── teams/
    ├── team-a/
    └── team-b/
```

### Avoid: Branch-per-Environment

Using branches for environments (dev, staging, prod) creates merge complexity and makes promotions difficult.

## Advanced Patterns (2025-2026)

### Multi-Cluster Management

- Hub-spoke architecture for fleet management
- Single ArgoCD instance managing 100+ clusters
- Cluster fleet provisioning and bootstrapping

### Progressive Delivery

- Canary deployments with automated rollback
- Blue-green with traffic shifting
- ArgoCD + Helm + Flagger integration
- AI-powered deployment (Akuity AI): auto-rollback on anomaly detection

### Environment Promotion

```
Feature Branch → Dev → Staging → Production
        ↓          ↓        ↓          ↓
    PR Review   Auto    Manual    Manual
                        Approval  Approval
```

## Industry Stats (2025-2026)

| Metric | Value |
|--------|-------|
| K8s deployments using GitOps | 90%+ |
| Organizations planning to continue/increase GitOps | 93% |
| Adopters reporting higher reliability | 80%+ |
| Organizations that adopted GitOps (mid-2025) | Two-thirds |
| ArgoCD market share | ~60% |

## Implementation Phases

| Phase | Activities |
|-------|------------|
| **Phase 1** | Assess current state, design target architecture |
| **Phase 2** | Basic GitOps setup, single environment |
| **Phase 3** | Multi-environment, security/compliance integration |
| **Phase 4** | Multi-cluster management, progressive delivery |
| **Phase 5** | Self-service developer platforms, advanced automation |

## Best Practices Summary

1. **Separate CI from CD** - Build/test in CI, deploy via GitOps
2. **Use drift detection** - Enable auto-remediation
3. **Implement progressive delivery** - Canary, blue-green
4. **DRY configuration** - Use Kustomize overlays or Helm values
5. **Secure secrets** - Use SOPS, Sealed Secrets, or external vaults
6. **Environment promotion via PRs** - Not direct pushes

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Set up GitHub Actions workflow from template | haiku | Pattern application, simple configuration |
| Design CI/CD pipeline architecture | opus | Complex system design with many variables |
| Write terraform code for infrastructure | sonnet | Implementation with moderate complexity |
| Debug failing pipeline step | sonnet | Debugging and problem-solving |
| Implement AIOps anomaly detection | opus | Novel ML approach, complex decision |
| Configure webhook and secret management | haiku | Mechanical setup using checklists |


## Sources

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Flux Documentation](https://fluxcd.io/docs/)
- [CNCF GitOps Working Group](https://github.com/open-gitops/documents)
- [Akuity Platform](https://akuity.io/)
- [GitOps Best Practices - Akuity](https://akuity.io/blog/gitops-best-practices-whitepaper)
- [CNCF GitOps 2025](https://www.cncf.io/blog/2025/06/09/gitops-in-2025-from-old-school-updates-to-the-modern-way/)
- [GitOps Repository Structure - Medium](https://medium.com/google-cloud/the-gitops-repository-structure-monorepo-vs-polyrepo-and-best-practices-17399ae6f3f4)
- [Flux Repository Structure Guide](https://fluxcd.io/flux/guides/repository-structure/)

---

*GitOps Methodology | faion-cicd-engineer | 2025-2026*
