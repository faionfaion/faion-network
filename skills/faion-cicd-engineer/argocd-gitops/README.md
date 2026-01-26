# ArgoCD GitOps

## Overview

ArgoCD is a declarative GitOps continuous delivery tool for Kubernetes. It synchronizes application state from Git repositories to Kubernetes clusters, providing automated deployment, drift detection, and rollback capabilities.

**Adoption:** Used in ~60% of Kubernetes clusters (CNCF 2025 survey).

## When to Use

| Scenario | Fit |
|----------|-----|
| Kubernetes-native deployments | Excellent |
| Git as source of truth | Excellent |
| Multi-cluster deployments | Excellent |
| Progressive delivery | Good (with Argo Rollouts) |
| Non-K8s workloads | Not suitable |

## Key Concepts

| Concept | Description |
|---------|-------------|
| Application | ArgoCD resource defining source and destination |
| Project | Logical grouping with RBAC |
| Repository | Git repo with K8s manifests |
| Sync | Applying Git state to cluster |
| Health | Application health assessment |
| Refresh | Comparing Git vs cluster state |
| ApplicationSet | Template for generating multiple Applications |

## GitOps Flow

```
Git Repository  <-->  ArgoCD Controller  <-->  Kubernetes Cluster
      ^                      |
      |                      v
  CI Pipeline          Metrics/Alerts
```

## Core Components

| Component | Purpose | Scaling |
|-----------|---------|---------|
| argocd-server | API/UI server | 2-5 replicas |
| argocd-repo-server | Git operations | 2-5 replicas |
| argocd-controller | Reconciliation | 1 replica (HA: sharding) |
| argocd-applicationset-controller | ApplicationSet processing | 2 replicas |
| argocd-notifications | Alerting | 1 replica |

## Best Practices Summary

1. **Separate repos** - App code and GitOps config in different repos
2. **Folders over branches** - Use folders for environments, not branches
3. **Use Helm/Kustomize** - Never manage raw YAML directly
4. **ApplicationSets** - Automate multi-env/cluster deployments
5. **Sync waves** - Control deployment order
6. **RBAC via AppProjects** - Per-tenant isolation
7. **Notifications** - Alert on sync failures
8. **Sync windows** - Prevent deployments during maintenance

## Anti-Patterns to Avoid

| Anti-Pattern | Why Bad | Solution |
|--------------|---------|----------|
| Raw YAML management | Duplication, drift | Use Helm/Kustomize |
| kubectl in production | Breaks GitOps | All changes via Git |
| Same repo for code+config | Infinite CI loops | Separate repos |
| Branches for environments | Merge conflicts | Use folders |
| Single ArgoCD for 100+ clusters | Performance issues | Shard or multiple instances |
| No sync windows | Uncontrolled prod changes | Define maintenance windows |

## File Structure

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Production-ready examples |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | AI assistant prompts |

## References

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [ArgoCD Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
- [ApplicationSet Documentation](https://argo-cd.readthedocs.io/en/stable/user-guide/application-set/)
- [Codefresh ArgoCD Best Practices](https://codefresh.io/blog/argo-cd-best-practices/)
- [ArgoCD Anti-Patterns](https://codefresh.io/blog/argo-cd-anti-patterns-for-gitops/)
- [OpenShift GitOps Practices](https://developers.redhat.com/blog/2025/03/05/openshift-gitops-recommended-practices)
- [GitOps Tools 2026](https://spacelift.io/blog/gitops-tools)

---

*ArgoCD GitOps Methodology | faion-cicd-engineer*
