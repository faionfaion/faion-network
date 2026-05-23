---
slug: devops-lb-health-checks
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates an LB health-check spec: liveness vs readiness endpoints, dependency checks, tuned interval/fall/rise parameters, language-specific implementation skeletons (Go / FastAPI / Node).
content_id: "6ad7131c85a4e5e9"
complexity: medium
produces: config
est_tokens: 4300
tags: [health-checks, liveness, readiness, load-balancer, reliability]
---
# Load Balancer Health Checks

## Summary

**One-sentence:** Generates an LB health-check spec: liveness vs readiness endpoints, dependency checks, tuned interval/fall/rise parameters, language-specific implementation skeletons (Go / FastAPI / Node).

**One-paragraph:** Generates an LB health-check spec: liveness vs readiness endpoints, dependency checks, tuned interval/fall/rise parameters, language-specific implementation skeletons (Go / FastAPI / Node). The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Розділення `/healthz` (liveness) і `/ready` (readiness) для rolling deploys.
- Dependency checks (DB ping + Redis ping) в readiness, не в liveness.
- Tuning `interval`/`unhealthy_threshold`/`healthy_threshold` під SLO.
- Probe skeletons на Go/Python/Node з proper timeouts.

## Applies If (ALL must hold)

- Application is multi-instance behind any LB (HAProxy / cloud ALB / k8s Service).
- Backend exposes at least one process or dependency that can fail independently.
- Rolling deployment or autoscaling will be used (≥1 deploy per week).

## Skip If (ANY kills it)

- Single-instance app with no upstream LB.
- Backend has zero external dependencies and zero restart logic — TCP-only check is acceptable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Dependency list | table (name, criticality, ping path) | Application team |
| Deploy cadence | frequency per week | SRE |
| SLO error budget | % allowed downtime per month | SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/devops-lb-algorithms/AGENTS.md` | LB layer context |

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
| `draft-devops-lb-health-checks` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-lb-health-checks.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[devops-lb-haproxy]]
- [[devops-lb-kubernetes]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
