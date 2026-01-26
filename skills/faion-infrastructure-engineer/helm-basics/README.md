---
id: helm-basics
name: "Helm Basics"
domain: OPS
skill: faion-infrastructure-engineer
category: "devops"
version: "2.0.0"
updated: "2026-01"
---

# Helm Basics

## Overview

Helm is the package manager for Kubernetes, enabling templating, versioning, and sharing of Kubernetes manifests. Charts bundle related resources into reusable, configurable packages with dependency management and release lifecycle control.

## When to Use

- Deploying complex applications with many Kubernetes resources
- Managing multiple environments (dev, staging, prod) with different configurations
- Creating reusable deployment packages
- Implementing GitOps workflows
- Sharing applications across teams or organizations
- Standardizing Kubernetes deployments across organization

## Key Concepts

| Concept | Description |
|---------|-------------|
| Chart | Package containing Kubernetes resource templates |
| Release | Instance of a chart running in cluster |
| Values | Configuration parameters for customizing charts |
| Template | Go template files generating Kubernetes manifests |
| Repository | Collection of published charts |
| Hook | Actions at specific release lifecycle points |
| Library Chart | Reusable templates shared across charts (not deployed directly) |

## Chart Types

| Type | Purpose | Deployable |
|------|---------|------------|
| Application | Complete, deployable solutions | Yes |
| Library | Shared templates and functions | No |

Library charts (like Bitnami Common Chart) provide abstraction for common patterns across repositories.

## Chart Structure

```
mychart/
├── Chart.yaml          # Chart metadata (required)
├── Chart.lock          # Dependency lock file
├── values.yaml         # Default configuration (required)
├── values.schema.json  # JSON Schema for values validation
├── templates/          # Kubernetes manifest templates
│   ├── NOTES.txt       # Post-install notes (user-facing)
│   ├── _helpers.tpl    # Template helpers (no output)
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   ├── pdb.yaml
│   ├── networkpolicy.yaml
│   ├── serviceaccount.yaml
│   └── tests/
│       └── test-connection.yaml
├── charts/             # Dependency charts
└── crds/               # Custom Resource Definitions
```

## Essential Commands

### Chart Development

```bash
# Create new chart
helm create mychart

# Lint chart (validate structure)
helm lint ./mychart

# Template locally (dry-run, see output)
helm template myrelease ./mychart -f values-prod.yaml

# Validate before install
helm install myrelease ./mychart --dry-run --debug

# Update dependencies
helm dependency update ./mychart
```

### Release Management

```bash
# Install chart
helm install myrelease ./mychart \
  --namespace myapp \
  --create-namespace \
  -f values-prod.yaml

# Upgrade release (atomic = auto-rollback on failure)
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

# Rollback to previous revision
helm rollback myrelease 1 --namespace myapp

# List releases
helm list --namespace myapp

# Get release history
helm history myrelease --namespace myapp

# Uninstall
helm uninstall myrelease --namespace myapp
```

### Repository Management

```bash
# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Search charts
helm search repo postgresql

# Package chart
helm package ./mychart --version 1.0.0

# Push to OCI registry
helm push mychart-1.0.0.tgz oci://registry.example.com/charts
```

## Core Principles

### DRY (Don't Repeat Yourself)

Eliminate manifest duplication across environments using a single chart template with environment-specific values files.

### YAGNI (You Ain't Gonna Need It)

Avoid over-parameterization. Only create template functions and conditionals for real, current problems - not hypothetical scenarios.

### One Chart Per Application

Maintain one Helm Chart per application to simplify ownership and limit failure impact.

## Best Practices Summary

| Category | Practice |
|----------|----------|
| Structure | One chart per application, separate templates by resource type |
| Values | Group related values, use descriptive names, environment-specific files |
| Templates | Minimal conditional logic, feature flags for optional resources |
| Naming | Include release and chart names in resource identifiers |
| Versioning | Semantic versioning (patch/minor/major) |
| Security | Never store secrets in values, use external secret managers |
| Testing | Run lint, template, dry-run before every deployment |
| Documentation | Document required values, optional features, upgrade notes |

## Related Documentation

| Document | Purpose |
|----------|---------|
| [checklist.md](checklist.md) | Pre-deployment verification |
| [examples.md](examples.md) | Common patterns and code samples |
| [templates.md](templates.md) | Starter templates for new charts |
| [llm-prompts.md](llm-prompts.md) | AI prompts for Helm tasks |

## References

- [Helm Documentation](https://helm.sh/docs/)
- [Chart Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Chart Template Guide](https://helm.sh/docs/chart_template_guide/)
- [Chart Development Tips](https://helm.sh/docs/howto/charts_tips_and_tricks/)
- [Artifact Hub](https://artifacthub.io/)

## Sources

- [Helm Official Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Helm Charts: Development Practices (2025)](https://carlosneto.dev/blog/2025/2025-02-25-helm-best-practices/)
- [Helm Chart Best Practices - DEV Community (2026)](https://dev.to/atmosly/helm-chart-best-practices-what-every-devops-engineer-should-know-4eeb)
- [Helm Chart Structure Cheat Sheet (2025)](https://sheetly.org/cheatsheets/helm-chart-structure)
- [Working with Helm Values - Komodor (2025)](https://komodor.com/learn/working-with-helm-values-common-operations-and-best-practices/)
