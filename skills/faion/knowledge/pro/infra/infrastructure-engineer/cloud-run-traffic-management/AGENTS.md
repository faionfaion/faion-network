---
slug: cloud-run-traffic-management
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Cloud Run traffic management: blue-green deployments, canary rollouts, gradual traffic shifting, rollback procedures, revision tagging, and Cloud Build CI/CD integration.
content_id: "785f79fcc0dae721"
complexity: medium
produces: config
est_tokens: 4100
tags: [gcp, cloud-run, traffic-management, blue-green, canary]
---
# Cloud Run Traffic Management

## Summary

**One-sentence:** Cloud Run traffic management: blue-green deployments, canary rollouts, gradual traffic shifting, rollback procedures, revision tagging, and Cloud Build CI/CD integration.

**One-paragraph:** Cloud Run supports revision-based traffic splitting: deploy a new revision without traffic, test it via a tagged URL, then gradually shift traffic using update-traffic commands. Revisions are immutable; rollback is instant via --to-revisions pointing to a prior revision. Tags give stable preview URLs independent of traffic allocation.

**Ефективно для:**

- Поетапний rollout нової ревізії з канарковим traffic split (1% → 100%).
- Blue/green з миттєвим rollback через ревізії з tag.
- Передпрод-перевірка нової ревізії на tagged URL без traffic.
- A/B експерименти між двома ревізіями зі стабільним розподілом.

## Applies If (ALL must hold)

- Releasing a new version of a Cloud Run service with zero-downtime.
- Testing a new revision before routing production traffic to it.
- Implementing canary releases with gradual traffic percentages.
- Rolling back a bad deployment to a prior revision instantly.
- Running A/B tests across two revisions of the same service.

## Skip If (ANY kills it)

- Single-revision dev environment without traffic splitting.
- Jobs (no traffic concept) — use Cloud Run Jobs methodology.
- Non-Cloud-Run targets (e.g. GKE) — use the relevant ingress/gateway methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Two or more revisions | deployed Cloud Run revisions | deploy pipeline |
| Rollout plan | canary / blue-green / a-b | release engineer |
| Smoke-test endpoint | URL or tagged URL | QA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gcp-cloud-run-serverless]] | Sibling methodology that supplies context required here. |
| [[cloud-run-deployment]] | Sibling methodology that supplies context required here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with statement + rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule id from 01-core-rules | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision tree application — needs nuance + context awareness. |
| `draft-config` | sonnet | Light judgement on field selection + naming conventions. |
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-cloud-run-traffic-management.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cloud-run-traffic-management.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cloud-run-traffic-management.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gcp-cloud-run-serverless]]
- [[cloud-run-deployment]]
- [[cloud-run-monitoring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. cloud-run-traffic-management vs an adjacent sibling).
