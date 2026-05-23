---
slug: devops-lb-high-availability
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates an LB high-availability design: HA topology (active-passive / active-active / anycast / DNS failover), cloud LB choice (ALB / NLB / GLB), and infra-as-code skeleton.
content_id: "aac341f8618e47c1"
complexity: deep
produces: decision-record
est_tokens: 4600
tags: [high-availability, anycast, vrrp, alb, nlb, cloud-lb]
---
# Load Balancer High Availability and Cloud Patterns

## Summary

**One-sentence:** Generates an LB high-availability design: HA topology (active-passive / active-active / anycast / DNS failover), cloud LB choice (ALB / NLB / GLB), and infra-as-code skeleton.

**One-paragraph:** Generates an LB high-availability design: HA topology (active-passive / active-active / anycast / DNS failover), cloud LB choice (ALB / NLB / GLB), and infra-as-code skeleton. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Per-region HA pair (keepalived + VRRP / floating VIP) на bare-metal.
- Multi-AZ cloud LB selection (ALB vs NLB vs GLB; GCP HTTPS LB; Azure Front Door).
- Active-active anycast для global traffic.
- DNS-failover як disaster-recovery fallback (Route 53 health checks).

## Applies If (ALL must hold)

- Service has an availability target (SLO) higher than what a single LB instance delivers.
- Failover behaviour (RTO/RPO) must be documented and tested.
- Either self-hosted HA pair OR cloud managed LB is on the table.

## Skip If (ANY kills it)

- Internal LB with no availability requirement.
- Single-region single-AZ deployment with no DR commitment.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Availability SLO | % per month | Business / SRE |
| Failure scenarios | table (scenario, RTO target) | SRE |
| Region/AZ inventory | list (region, az, capacity) | Platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/devops-lb-algorithms/AGENTS.md` | Layer + algorithm context |

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
| `draft-devops-lb-high-availability` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-lb-high-availability.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[devops-lb-algorithms]]
- [[devops-lb-haproxy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
