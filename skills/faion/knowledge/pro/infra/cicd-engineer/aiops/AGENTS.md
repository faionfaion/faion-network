---
slug: aiops
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Spec for an AIOps program \u2014 anomaly detection signals, promotion rules to incident, trust-tiered automated remediation, and outcome metrics (precision, auto-remediation rate, MTTR)."
content_id: "3746128199b2d58f"
complexity: deep
produces: spec
est_tokens: 5000
tags: [aiops, anomaly-detection, auto-remediation, mttr, ml, infra]
---
# AIOps Anomaly + Auto-remediation Playbook

## Summary

**One-sentence:** Spec for an AIOps program — anomaly detection signals, promotion rules to incident, trust-tiered automated remediation, and outcome metrics (precision, auto-remediation rate, MTTR).

**One-paragraph:** Spec for an AIOps program — anomaly detection signals, promotion rules to incident, trust-tiered automated remediation, and outcome metrics (precision, auto-remediation rate, MTTR). The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Service has ≥ 1 year of incident history to compute baselines from.
- Anomaly precision baseline exists or can be measured in first month.
- There is a named SRE owner accountable for remediation policy.

## Skip If (ANY kills it)

- Service is too small for ML-grade baselines.
- Team lacks budget + ownership for AIOps tooling.
- Incidents are dominated by external dependencies that AIOps cannot affect.

**Ефективно для:**

- Команди з > 50 incidents / квартал шукають MTTR drop.
- Splunk ITSI / Datadog AIOps / Dynatrace Davis середовища.
- ML-powered anomaly detection over baseline thresholds.
- Trust-tier policy: recommend-only → human-approved → autonomous.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev` | Parent role context. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aiops.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
