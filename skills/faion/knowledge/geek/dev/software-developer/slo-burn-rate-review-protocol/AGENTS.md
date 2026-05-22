---
slug: slo-burn-rate-review-protocol
tier: geek
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Weekly 30-min architect-led ritual converting SLO burn data + matrix-triggered actions into named ADR-worthy decisions captured in a versioned review note."
content_id: "60fca40b4cd4049d"
complexity: medium
produces: report
est_tokens: 4600
tags: [slo, error-budget, architecture, weekly-review, adr, burn-rate]
---

# SLO Burn-Rate Review Protocol

## Summary

**One-sentence:** Weekly 30-min architect-led ritual converting SLO burn data + matrix-triggered actions into named ADR-worthy decisions captured in a versioned review note.

**One-paragraph:** Weekly 30-min architect-led ritual converting SLO burn data + matrix-triggered actions into named ADR-worthy decisions captured in a versioned review note. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`report`) at a medium complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- SLOs are in use with burn-rate alerting in production.
- A burn decision matrix is in use (matrix-triggered actions logged).
- An architect or tech lead has authority to drive architectural decisions.
- At least one production service has ≥3 months of SLO history.

## Skip If (ANY kills it)

- No SLOs or no burn-rate alerts in use — the review has no data.
- Single-service shop with no architectural decisions to make — overhead exceeds value.
- Daily team meeting already absorbs burn signals adequately.
- Architecture changes are politically blocked — surfaced decisions go unactioned.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Burn-rate dashboards | Grafana / Honeycomb / Datadog | observability stack |
| Matrix-triggered actions log | JSON / Markdown audit | slo-burn-decision-matrix |
| Postmortem tracking | Jira / Linear / GitHub | incident-mgmt |
| 30-min weekly slot | calendar | architect + on-call lead + product rep |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/slo-definition-template-per-service-class` | Defines the SLOs being reviewed. |
| `pro/infra/devops-engineer/slo-burn-decision-matrix` | Supplies the actions log this review aggregates. |
| `pro/dev/software-architect/retro-adr-workflow` | Captures decisions arising from the review. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/05-examples.xml` | medium | One end-to-end worked example | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `data_prep_burn_trace` | haiku | Deterministic data pull |
| `agenda_pre_brief` | sonnet | Compose 5-item brief with current week evidence |
| `decision_capture_drafting` | sonnet | Write post-review decision log from notes |
| `adr_spawn_check` | opus | Decide whether the decision rises to ADR weight |

## Templates

| File | Purpose |
|------|---------|
| `templates/burn-review.md` | Weekly review note skeleton (5 sections + decision log block) |
| `templates/decision-log-entry.md` | Shape of one decision-log entry produced by the review |
| `templates/agenda-pre-brief.md` | 1-page brief sent 24h before the meeting |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-slo-burn-rate-review-protocol.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/dev/`
- `[[slo-definition-template-per-service-class]]`
- `[[slo-burn-decision-matrix]]`
- `[[retro-adr-workflow]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether slo-burn-rate-review-protocol applies: root question — "Did burn-rate alerts fire in the past week (or matrix actions were taken)?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
