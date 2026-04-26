# Helm Charts

## Summary

Helm is the package manager for Kubernetes (v4+ as of 2026). Charts bundle related K8s resources into configurable, versioned packages. Every production chart must include: resource requests/limits, HPA, PodDisruptionBudget, pod anti-affinity, all three health probes, and a non-root security context.

## Why

A 2025 analysis of 100+ open-source Helm charts found only 17% met production-reliability criteria (PDB, anti-affinity, HPA). Authoring charts with these elements from the start avoids emergency retrofits under load. `values.schema.json` validation catches misconfiguration before apply.

## When To Use

- Complex applications with many K8s resources across multiple environments
- Reusable deployment packages shared across teams or clusters
- GitOps workflows (ArgoCD, Flux) where charts are the unit of change
- Multi-environment deploys with per-environment `values-{env}.yaml` files

## When NOT To Use

- Quick experiments or learning — plain YAML is simpler
- Small, static setups with no variation across environments — use Kustomize
- Single-resource deployments — overhead not justified
- When you want Helm to manage secrets — use External Secrets Operator instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-chart-structure.xml` | Chart.yaml fields, directory layout, naming conventions, dependency management |
| `content/02-reliability-security.xml` | Production checklist: HPA, PDB, anti-affinity, probes, security context rules |
| `content/03-examples.xml` | values.yaml production example, values-dev/prod overrides, schema validation |

## Templates

| File | Purpose |
|------|---------|
| `templates/_helpers.tpl` | Standard Go template helpers: name, fullname, labels, selectorLabels, image, configChecksum |
| `templates/deployment.yaml` | Production deployment template with all reliability and security fields |
| `templates/hpa.yaml` | HorizontalPodAutoscaler template |
| `templates/pdb.yaml` | PodDisruptionBudget template |
| `templates/values.schema.json` | JSON Schema for values validation |
| `templates/prompt-create-chart.txt` | LLM prompt to create a production-ready Helm chart |
