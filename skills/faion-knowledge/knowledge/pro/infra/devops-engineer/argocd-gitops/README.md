# ArgoCD GitOps

## Overview

ArgoCD is a declarative GitOps continuous delivery tool for Kubernetes. It synchronizes application state from Git repositories to Kubernetes clusters, providing automated deployment, drift detection, and rollback capabilities.

## When to Use

| Scenario | ArgoCD Fit |
|----------|-----------|
| Kubernetes-native deployments | Excellent |
| GitOps workflows (Git as source of truth) | Excellent |
| Multi-cluster deployments | Excellent |
| Progressive delivery with Argo Rollouts | Excellent |
| Teams requiring deployment visibility | Good |
| Non-Kubernetes deployments | Not suitable |

## Key Concepts

| Concept | Description |
|---------|-------------|
| Application | ArgoCD resource defining source and destination |
| Project | Logical grouping of applications with RBAC |
| ApplicationSet | Template for generating multiple applications |
| Repository | Git repo containing Kubernetes manifests |
| Sync | Process of applying Git state to cluster |
| Health | Application health status assessment |
| Refresh | Comparing Git state with cluster state |
| Rollback | Reverting to previous Git commit |

## GitOps Flow

```
Git Repository  <-->  ArgoCD Controller  <-->  Kubernetes Cluster
      ^                      |
      |                      v
CI Pipeline            Metrics/Alerts
```

## Architecture Patterns

### Hub and Spoke (Centralized)

Single ArgoCD instance manages multiple clusters.

| Pros | Cons |
|------|------|
| Single pane of glass | Scaling challenges |
| Simplified management | Single point of failure |
| Reduced operational overhead | Network connectivity requirements |

### Standalone (Distributed)

Each cluster has its own ArgoCD instance.

| Pros | Cons |
|------|------|
| Better isolation | Multiple instances to manage |
| Independent scaling | Increased complexity |
| No cross-cluster network requirements | No centralized view |

## Sync Strategies

| Strategy | Use Case | Configuration |
|----------|----------|---------------|
| Manual | Production with strict change control | `automated: false` |
| Automated | Dev/staging rapid iteration | `automated: true` |
| Auto + Self-Heal | Drift correction required | `selfHeal: true` |
| Auto + Prune | Clean up deleted resources | `prune: true` |

## Repository Structure

```
kubernetes-manifests/
├── apps/
│   └── {app-name}/
│       ├── base/
│       │   ├── kustomization.yaml
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   └── configmap.yaml
│       └── overlays/
│           ├── staging/
│           │   └── kustomization.yaml
│           └── production/
│               └── kustomization.yaml
├── infrastructure/
│   ├── cert-manager/
│   ├── ingress-nginx/
│   └── external-secrets/
└── projects/
    ├── team-a.yaml
    └── team-b.yaml
```

## Best Practices Summary

1. **Separate config from source code** - Use dedicated GitOps repository
2. **Use folders not branches** - Model environments with folders
3. **Use ApplicationSets** - Automate multi-environment deployments
4. **Implement RBAC via Projects** - Scope access per team
5. **Configure sync windows** - Prevent deployments during incidents
6. **Enable notifications** - Alert on sync failures
7. **Use Kustomize/Helm** - Avoid raw YAML duplication
8. **Secure secrets** - Use External Secrets, Sealed Secrets, or Vault
9. **Enable self-heal** - Maintain desired state automatically
10. **Monitor with metrics** - Track sync status and health

## Folder Contents

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts |
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Complete code examples |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for ArgoCD tasks |

## Related Tools

| Tool | Purpose |
|------|---------|
| Argo Rollouts | Progressive delivery (canary, blue-green) |
| External Secrets | Secrets management |
| Kustomize | Configuration management |
| Helm | Package management |
| Crossplane | Infrastructure as Code |

## References

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [ArgoCD Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
- [ApplicationSet Documentation](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/)
- [Argo Rollouts](https://argoproj.github.io/rollouts/)
- [Codefresh ArgoCD Best Practices](https://codefresh.io/blog/argo-cd-best-practices/)
- [Red Hat OpenShift GitOps](https://developers.redhat.com/blog/2025/03/05/openshift-gitops-recommended-practices)

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Run terraform plan, docker build, kubectl get commands | haiku | Mechanical CLI operations |
| Review Dockerfile for best practices | sonnet | Code review, security patterns |
| Debug pod crashes, container networking issues | sonnet | Diagnosis and error analysis |
| Design multi-region failover architecture | opus | Complex distributed systems decisions |
| Write Helm values for production rollout | sonnet | Configuration and templating |
| Create monitoring strategy for microservices | opus | System-wide observability design |
| Troubleshoot Kubernetes pod evictions under load | sonnet | Performance debugging and analysis |
