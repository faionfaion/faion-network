---
slug: feature-flag-rollout-runbook
tier: geek
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Staged feature-flag rollout runbook: 1/10/50/100% cohorts, kill switch, SLO-tied auto-rollback, flag-cleanup TODO, post-rollout audit."
content_id: "f2894943924cf018"
complexity: medium
produces: playbook-step
est_tokens: 3800
tags: [feature-flags, rollout, progressive-delivery, kill-switch, geek, infra]
---

# Feature Flag Rollout Runbook

## Summary

**One-sentence:** Staged feature-flag rollout runbook: 1/10/50/100% cohorts, kill switch, SLO-tied auto-rollback, flag-cleanup TODO, post-rollout audit.

**One-paragraph:** Staged feature-flag rollout runbook: 1/10/50/100% cohorts, kill switch, SLO-tied auto-rollback, flag-cleanup TODO, post-rollout audit. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`playbook-step`) at a medium complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Feature flag system is in use (LaunchDarkly / Unleash / OpenFeature / homegrown).
- Feature rollout affects ≥1% of live production traffic.
- An on-call rotation exists to receive auto-rollback alerts.

## Skip If (ANY kills it)

- Internal-only feature with <10 users — full rollout is fine.
- Pre-production prototype — no users to stage against.
- Hard-gated feature for one customer — flag is just a release marker; full rollout to that account.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Feature flag platform | LaunchDarkly / Unleash / OpenFeature | infra |
| SLO + alerting | Prom / Datadog / Honeycomb | slo-definition-template-per-service-class |
| Kill switch | feature flag boolean | infra |
| Cohort definitions | Markdown / flag config | product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/progressive-delivery-101` | Foundational concept. |
| `pro/infra/devops-engineer/slo-definition-template-per-service-class` | Source of rollback SLO thresholds. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cohort_definition` | sonnet | Cohort math: 1/10/50/100% on a stable hash. |
| `auto_rollback_wiring` | sonnet | Wire alert → flag flip. |
| `post_rollout_audit` | haiku | Mechanical cleanup checks. |

## Templates

| File | Purpose |
|------|---------|
| `templates/runbook.md` | Full rollout runbook with 1/10/50/100 stages + abort criteria. |
| `templates/auto-rollback-alert.yaml` | Alert manager / Datadog monitor template. |
| `templates/post-rollout-audit.md` | Cleanup checklist + flag-removal PR template. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feature-flag-rollout-runbook.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[progressive-delivery-101]]`
- `[[slo-definition-template-per-service-class]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether feature-flag-rollout-runbook applies: root question — "Does this rollout touch ≥1% of live traffic AND a feature flag platform is available?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
