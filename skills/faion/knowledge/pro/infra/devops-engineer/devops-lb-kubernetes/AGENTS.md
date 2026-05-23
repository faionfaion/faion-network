---
slug: devops-lb-kubernetes
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a Kubernetes load-balancing spec: Service type per workload, Ingress controller choice (Nginx/Traefik/AWS ALB Controller), readiness+liveness probes, and rolling-update guards.
content_id: "36d272cd375321cf"
complexity: medium
produces: config
est_tokens: 4400
tags: [kubernetes, ingress, service, probes, load-balancing]
---
# Kubernetes Load Balancing: Services, Ingress, Probes

## Summary

**One-sentence:** Generates a Kubernetes load-balancing spec: Service type per workload, Ingress controller choice (Nginx/Traefik/AWS ALB Controller), readiness+liveness probes, and rolling-update guards.

**One-paragraph:** Generates a Kubernetes load-balancing spec: Service type per workload, Ingress controller choice (Nginx/Traefik/AWS ALB Controller), readiness+liveness probes, and rolling-update guards. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Перший Ingress setup в кластері — вибір контролера (Nginx vs Traefik vs ALB Controller).
- ClusterIP vs NodePort vs LoadBalancer Service — обґрунтований дизайн.
- Probe-driven rolling deploys без traffic drop.
- Host/path TLS termination через cert-manager + ingress class.

## Applies If (ALL must hold)

- Workload runs on a Kubernetes cluster (≥1 namespace in production scope).
- External traffic (or cross-namespace traffic) must reach pods.
- Rolling updates or autoscaling are part of the deployment model.

## Skip If (ANY kills it)

- Standalone pods with no Service (no LB needed).
- External LB is handled entirely outside Kubernetes (e.g. cloud ALB pointing at NodePort), and no Ingress is in scope.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service inventory | table (name, ns, expected QPS) | Platform |
| TLS strategy | passthrough / termination | Security |
| Ingress controller choice | free-form | Platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/devops-lb-health-checks/AGENTS.md` | Probe semantics |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-devops-lb-kubernetes` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-lb-kubernetes.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[devops-lb-health-checks]]
- [[devops-lb-ssl-tls]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
