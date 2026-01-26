---
id: helm-charts
name: "Helm Charts"
domain: OPS
skill: faion-devops-engineer
category: "devops"
version: "2.0.0"
updated: "2026-01"
---

# Helm Charts

Helm is the package manager for Kubernetes (v4.1.0 as of January 2026). Charts bundle related resources into reusable, configurable packages with dependency management and release lifecycle control.

## When to Use

| Scenario | Recommended |
|----------|-------------|
| Complex applications with many K8s resources | Helm |
| Multiple environments (dev, staging, prod) | Helm |
| Reusable deployment packages | Helm |
| GitOps workflows | Helm |
| Quick experiments, learning | Plain YAML |
| Small setups with limited variation | Kustomize |

## Key Concepts

| Concept | Description |
|---------|-------------|
| Chart | Package containing Kubernetes resource templates |
| Release | Instance of a chart running in cluster |
| Values | Configuration parameters for customizing charts |
| Template | Go template files generating Kubernetes manifests |
| Repository | Collection of published charts |
| Hook | Actions at specific release lifecycle points |
| OCI Registry | Modern chart storage using container registries |

## Chart Structure

```
mychart/
├── Chart.yaml          # Chart metadata (required)
├── Chart.lock          # Dependency lock file
├── values.yaml         # Default configuration (required)
├── values.schema.json  # JSON Schema for values validation
├── templates/          # Kubernetes manifest templates
│   ├── NOTES.txt       # Post-install notes
│   ├── _helpers.tpl    # Template helpers
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   ├── pdb.yaml        # Pod Disruption Budget
│   ├── networkpolicy.yaml
│   └── tests/
│       └── test-connection.yaml
├── charts/             # Dependency charts
└── crds/               # Custom Resource Definitions
```

## Essential Commands

```bash
# Create new chart
helm create mychart

# Lint chart
helm lint ./mychart

# Template locally (dry-run)
helm template myrelease ./mychart -f values-prod.yaml

# Install chart
helm install myrelease ./mychart \
  --namespace myapp \
  --create-namespace \
  -f values-prod.yaml

# Upgrade release (atomic = rollback on failure)
helm upgrade myrelease ./mychart \
  --namespace myapp \
  -f values-prod.yaml \
  --atomic \
  --timeout 5m

# Install or upgrade (idempotent)
helm upgrade --install myrelease ./mychart \
  --namespace myapp \
  --create-namespace \
  -f values-prod.yaml

# Rollback to revision
helm rollback myrelease 1 --namespace myapp

# List releases
helm list --namespace myapp

# Get release history
helm history myrelease --namespace myapp

# Uninstall
helm uninstall myrelease --namespace myapp

# Repository management
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Search charts
helm search repo postgresql

# Update dependencies
helm dependency update ./mychart

# Package chart
helm package ./mychart --version 1.0.0

# Push to OCI registry
helm push mychart-1.0.0.tgz oci://registry.example.com/charts
```

## Reliability Statistics (2025 Study)

A 2025 analysis of 100+ open-source Helm charts found:

| Metric | Finding |
|--------|---------|
| "Reliable" tier (7+ criteria) | 17.1% (18 charts) |
| Highest score | 9/10 (no perfect 10) |
| Common gaps | PDB, anti-affinity, HPA |

**Key insight:** Do not assume a chart is production-ready just because it's popular.

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and commands |
| [checklist.md](checklist.md) | Production readiness checklist |
| [examples.md](examples.md) | Chart.yaml, values.yaml, templates |
| [templates.md](templates.md) | Reusable template patterns |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for Helm tasks |

## References

- [Helm Documentation](https://helm.sh/docs/)
- [Chart Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Artifact Hub](https://artifacthub.io/)
- [Helm Charts 2025 Guide](https://atmosly.com/knowledge/helm-charts-in-kubernetes-definitive-guide-for-2025)
- [Helm Reliability Study 2025](https://www.prequel.dev/blog-post/the-real-state-of-helm-chart-reliability-2025-hidden-risks-in-100-open-source-charts)
