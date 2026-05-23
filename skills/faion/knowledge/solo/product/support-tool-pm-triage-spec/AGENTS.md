---
slug: support-tool-pm-triage-spec
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Opinionated Intercom / Pylon / Zendesk triage spec: 5 tag categories, escalation rules, weekly digest format, named owner — converts support inbox into a defensible PM signal feed.
content_id: "94108ffdce9cf2c5"
complexity: light
produces: spec
est_tokens: 3500
tags: [support-tool-pm-triage-spec, intercom, pylon, feedback-pipeline]
---
# Support Tool Pm Triage Spec

## Summary

**One-sentence:** Opinionated Intercom / Pylon / Zendesk triage spec: 5 tag categories, escalation rules, weekly digest format, named owner — converts support inbox into a defensible PM signal feed.

**One-paragraph:** Opinionated Intercom / Pylon / Zendesk triage spec: 5 tag categories, escalation rules, weekly digest format, named owner — converts support inbox into a defensible PM signal feed. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Support Tool Pm Triage Spec on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- PM spends ≥3 hours / week in support tool.
- Support tool supports custom tags + saved views.
- ≥10 inbound conversations / week.
- Owner controls the tag taxonomy.

## Skip If (ANY kills it)

- Pre-launch, no real support volume.
- Support outsourced — different ownership.
- Single-channel only (email-only) with low volume.
- Tag schema already exists and works.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Support tool admin access | credentials | Intercom / Pylon |
| Existing tag inventory (if any) | export | Tool |
| PM time-box for triage | calendar slot | Self |
| Digest channel (Discord / email) | config | Self |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-operations/feedback-management` | Downstream consumer of digest. |
| `solo/product/product-planning/verbatim-to-backlog-pattern` | Converts digest into backlog. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-support-tool-pm-triage-spec` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-support-tool-pm-triage-spec` | haiku | Schema check + threshold checks; deterministic. |
| `review-support-tool-pm-triage-spec` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/support-tool-pm-triage-spec.json` | JSON skeleton conforming to the output contract schema. |
| `templates/support-tool-pm-triage-spec.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-support-tool-pm-triage-spec.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[feedback-management]]
- [[verbatim-to-backlog-pattern]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
