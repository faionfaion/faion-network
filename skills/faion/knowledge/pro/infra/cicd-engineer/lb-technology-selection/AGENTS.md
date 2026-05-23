---
slug: lb-technology-selection
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a decision-record naming the LB technology (HAProxy / Nginx / cloud-managed / K8s ingress) based on layer, environment, scale, and ops capacity.
content_id: "3c00bbfef4264fc1"
complexity: medium
produces: decision-record
est_tokens: 4400
tags: [load-balancing, technology-selection, haproxy, nginx, kubernetes]
---
# Load Balancer Technology Selection

## Summary

**One-sentence:** Generates a decision-record naming the LB technology (HAProxy / Nginx / cloud-managed / K8s ingress) based on layer, environment, scale, and ops capacity.

**One-paragraph:** Choose the right load balancer for production using a decision matrix covering HAProxy, Nginx, AWS/GCP/Azure managed LBs, and Kubernetes Ingress controllers. Selection criteria: traffic type (L4 / L7), environment (bare-metal / cloud / K8s), concurrency, operational complexity, and whether a managed product can do the job. The output is a decision record pointing to one of the downstream methodologies (lb-haproxy-production, lb-nginx-production, lb-cloud-terraform, lb-kubernetes-ingress).

**Ефективно для:**

- New service fleet: вибрати LB-стек з нуля одним рішенням.
- Migration single → multi-backend: визначити proper LB, не "за звичкою".
- Managed cloud LB vs self-hosted — оцінити operational + cost tradeoff.
- Bare-metal K8s: HAProxy / MetalLB / ingress-nginx — комбінація.
- Architecture review: відхилити "HAProxy для greenfield на GitHub з керованим cloud".

## Applies If (ALL must hold)

- Starting a new service fleet and selecting the LB stack from scratch.
- Migrating from a single-instance setup to a multi-backend load-balanced architecture.
- Evaluating whether to use a managed cloud LB or a self-hosted solution.
- Choosing a Kubernetes Ingress controller for a new cluster.

## Skip If (ANY kills it)

- Internal service-to-service mesh routing — use a service mesh (Linkerd, Istio, Cilium).
- Static-site CDN — Cloudflare / CloudFront / Fastly already serves this role.
- Single-instance dev workloads — `nginx -t` and `docker run -p` are sufficient.
- Database load balancing (PgBouncer, ProxySQL, Vitess) — use DB-specific patterns.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Hosting environment | aws/gcp/azure/bare-metal/k8s | infra |
| Traffic profile | L4 / L7 + qps | product / load test |
| Operational capacity | team size + on-call coverage | engineering |
| Existing investment | current LB inventory | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lb-layer-selection]] | The layer decision (L4/L7/hybrid) feeds the technology decision. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: managed-default-on-cloud, kubernetes-uses-ingress, bare-metal-uses-haproxy-or-nginx, layer-matches-tech, operational-capacity-gates-self-hosted | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for decision-record + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `analyze-environment` | sonnet | Combine hosting + scale + team. |
| `pick-technology` | sonnet | Decision-tree application. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tech-decision-record.md` | ADR skeleton: environment → tech → downstream methodology pointer |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-technology-selection.py` | Validate the tech-decision-record artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[lb-layer-selection]]
- [[lb-haproxy-production]]
- [[lb-nginx-production]]
- [[lb-cloud-terraform]]
- [[lb-kubernetes-ingress]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (cloud/bare-metal/K8s, layer, ops capacity) to a technology, each leaf referencing a rule from `01-core-rules.xml`.
