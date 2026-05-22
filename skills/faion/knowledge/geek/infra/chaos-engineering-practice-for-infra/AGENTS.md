---
slug: chaos-engineering-practice-for-infra
tier: geek
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Production-safe chaos engineering programme: hypothesis-driven experiments, blast-radius gating, GameDay cadence, learning capture, regression test conversion."
content_id: "d8aa195cb3bec879"
complexity: medium
produces: playbook-step
est_tokens: 3800
tags: [chaos, resilience, gameday, sre, infra, geek]
---

# Chaos Engineering Practice for Infra

## Summary

**One-sentence:** Production-safe chaos engineering programme: hypothesis-driven experiments, blast-radius gating, GameDay cadence, learning capture, regression test conversion.

**One-paragraph:** Production-safe chaos engineering programme: hypothesis-driven experiments, blast-radius gating, GameDay cadence, learning capture, regression test conversion. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`playbook-step`) at a medium complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Production system with availability SLO and ≥1 high-blast-radius dependency.
- Mature observability + incident response (mean detection time minutes-not-hours).
- Engineering org with capacity to act on chaos learnings.

## Skip If (ANY kills it)

- Pre-revenue prototype — chaos is overhead; fix obvious gaps first.
- Observability immature — cannot detect what chaos breaks; build observability first.
- Single-engineer service with no on-call — no team to act on learnings.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| SLO definitions | YAML / Markdown | slo-definition-template-per-service-class |
| Observability stack | Prom / Honeycomb / Datadog | platform |
| Incident response playbook | Markdown | incident-response-playbook |
| Blast-radius policy | Markdown | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/incident-response-playbook` | Defines incident response that chaos may invoke. |
| `pro/infra/devops-engineer/slo-definition-template-per-service-class` | Chaos thresholds derived from SLOs. |

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
| `hypothesis_drafting` | sonnet | Form per-experiment hypothesis with measurable predictions. |
| `blast_radius_gating` | opus | Multi-input safety check. |
| `learning_capture` | sonnet | Postmortem-style writeup from telemetry. |

## Templates

| File | Purpose |
|------|---------|
| `templates/experiment-card.md` | Single experiment hypothesis + abort criteria + blast radius. |
| `templates/gameday-agenda.md` | Quarterly GameDay agenda + scoring. |
| `templates/learning-log.md` | Per-experiment learning + regression test plan. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-chaos-engineering-practice-for-infra.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[incident-response-playbook]]`
- `[[slo-definition-template-per-service-class]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether chaos-engineering-practice-for-infra applies: root question — "Does the system have a live SLO + on-call rotation + working observability?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
