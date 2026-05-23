---
slug: lb-high-availability
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates an HA LB topology decision-record (active-pass/active-act, multi-AZ, anycast vs DNS GSLB, drain wiring) with explicit failure-domain analysis.
content_id: "f6f2a1b76778a0d3"
complexity: deep
produces: decision-record
est_tokens: 5200
tags: [load-balancing, high-availability, multi-region, gslb, infrastructure]
---
# Load Balancer High Availability Patterns

## Summary

**One-sentence:** Generates an HA LB topology decision-record (active-pass/active-act, multi-AZ, anycast vs DNS GSLB, drain wiring) with explicit failure-domain analysis.

**One-paragraph:** High availability for load-balanced systems requires redundancy at both the load balancer tier and the backend tier, distributed across availability zones or regions. Single-region HA uses active-active or active-passive LB pairs with zone-spread backends (≥ 2 LB instances + ≥ 2 AZs + ≥ 2 healthy backends per AZ). Multi-region HA adds Global Server Load Balancing (GSLB) — prefer anycast (AWS Global Accelerator, GCP Global LB, Cloudflare LB) over DNS-based GSLB when SLO ≥ 99.99%. Zero-downtime deployments require coordinated readiness-probe + connection-draining behaviour.

**Ефективно для:**

- Design новий service з SLA ≥ 99.9% — explicit failure-domain analysis.
- Multi-region failover з 99.99%+ SLA — anycast (НЕ DNS-based).
- Zero-downtime deploy: SIGTERM → 503 readiness → drain → exit.
- Post-incident review: знайти прихований SPOF (single LB, single-AZ backends).
- Add multi-region поверх існуючого single-region deployment.

## Applies If (ALL must hold)

- Designing a new load-balanced service with an availability SLA ≥ 99.9%.
- Reviewing an architecture proposal for hidden SPOFs at the load balancer tier.
- Planning a zero-downtime deployment or maintenance procedure.
- Adding multi-region failover to an existing single-region deployment.
- Post-incident review after a load balancer failure caused an outage.

## Skip If (ANY kills it)

- Development or staging environments where downtime is acceptable.
- Internal tools with no SLA — single instance is fine.
- Algorithm selection — see lb-algorithms.
- Health-check configuration depth — see lb-health-checks.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Availability SLA | percentage | product / SRE |
| Failure domain map | AZ / region inventory | infra |
| Per-tier instance counts | LB + backend per AZ | infra |
| Deployment strategy | rolling / blue-green / canary | release manager |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lb-health-checks]] | Readiness-probe behaviour underpins zero-downtime deploy. |
| [[lb-layer-selection]] | L4 vs L7 constrains the available HA primitives. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: two-lb-min, two-az-min, anycast-over-dns-for-9999, drain-on-sigterm, no-single-az-backends | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for decision-record + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked HA decision-record example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `failure-domain-analysis` | opus | High-judgement reasoning about hidden SPOFs. |
| `pick-gslb` | sonnet | Decision tree on SLO + provider. |
| `wire-drain-on-sigterm` | haiku | Mechanical code snippet. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ha-decision-record.md` | ADR skeleton: SLA → topology → failure modes → mitigations |
| `templates/sigterm-drain.py` | FastAPI graceful-shutdown handler |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-high-availability.py` | Validate the HA decision-record artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[lb-health-checks]]
- [[lb-layer-selection]]
- [[lb-cloud-terraform]]
- [[lb-haproxy-production]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (SLA target, geographic reach, infra ownership, deploy cadence) to a concrete HA topology, each leaf referencing a rule from `01-core-rules.xml`.
