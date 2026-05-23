---
slug: wcag-severity-rubric
tier: pro
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Three-axis triage rubric (assistive-tech blocker × WCAG level × user-journey criticality) that buckets a11y findings into blocker / serious / moderate / minor with SLAs.
content_id: "1353ca83c993209e"
complexity: medium
produces: rubric
est_tokens: 4100
tags: [accessibility, a11y, wcag, severity, triage, audit, rubric]
---
# WCAG Severity Rubric

## Summary

**One-sentence:** Three-axis triage rubric (assistive-tech blocker × WCAG level × user-journey criticality) that buckets a11y findings into blocker / serious / moderate / minor with SLAs.

**One-paragraph:** Three-axis triage rubric (assistive-tech blocker × WCAG level × user-journey criticality) that buckets a11y findings into blocker / serious / moderate / minor with SLAs. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-wcag-severity-rubric.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Post-audit triage коли VPAT/ACR returns 200+ findings і треба швидко вибрати fix order.
- Procurement / compliance gates (Section 508, EAA, ADA) з SLA per severity tier.
- QA-engineer організовує bug board і потрібен консистентний severity mapping.
- Roadmap-planning, де accessibility findings конкурують з feature work за пріоритет.

## Applies If (ALL must hold)

- Audit produced ≥20 findings that need prioritisation
- Team has WCAG knowledge (2.0 or 2.1, AA or AAA target)
- Findings include at-population context (which user journey, which AT, which device)
- Bug tracker supports severity field used by triage process

## Skip If (ANY kills it)

- <20 findings — triage by hand is faster than rubric overhead
- No assistive-technology testing was done — can't apply the AT-blocker axis
- Procurement context where the rubric must match the buyer's (use the buyer's)
- Pre-audit scoping phase — rubric is for outputs, not inputs

## Prerequisites

| Trigger artefact | format | author / source |
|---|---|---|
| Task brief | Markdown | requester |
| Named owner | string | requester / RACI |
| Prior artefact (if updating) | repo path | artefact store |
| Constraint inputs (budget, SLA, compliance) | structured | requester / policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/INDEX.xml` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology, each with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-wcag-severity-rubric` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rubric.json` | JSON instance with axis scores |
| `templates/rubric.md` | Rubric skeleton with weighted axes |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-wcag-severity-rubric.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[storybook-as-source-of-truth]]
- [[test-suite-audit-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
