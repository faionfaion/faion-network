---
slug: trust-boundary-diff-helper
tier: pro
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Compares pre/post-change trust boundaries (component list, ingress/egress edges, auth surfaces) and surfaces a security-review delta with risk-rated changes.
content_id: "3eb44b8d7f4ff4f9"
complexity: medium
produces: report
est_tokens: 4800
tags: [trust-boundary, diff, security, review, architect]
---
# Trust Boundary Diff Helper

## Summary

**One-sentence:** Compares pre/post-change trust boundaries (component list, ingress/egress edges, auth surfaces) and surfaces a security-review delta with risk-rated changes.

**One-paragraph:** Compares pre/post-change trust boundaries (component list, ingress/egress edges, auth surfaces) and surfaces a security-review delta with risk-rated changes. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-trust-boundary-diff-helper.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Architect security review of a new dependency / service edge.
- Pre/post-change comparison needed на short cycle (per PR / per release).
- Trust boundaries вже modelled (e.g. STRIDE TM or DFD) — diff is mechanical.
- Procurement / security audit gate потребує delta artefact, не full re-TM.

## Applies If (ALL must hold)

- Both pre-change and post-change trust-boundary descriptions available
- Trust-boundary representation is consistent (same notation, same granularity)
- Change touches ingress, egress, or auth surface
- Diff will drive a review or audit decision

## Skip If (ANY kills it)

- No baseline trust-boundary model exists — model first, then diff
- Change is purely internal (no boundary impact) — diff is empty
- Diff will not be acted on — overhead unjustified
- Boundary representation changed between versions (notation mismatch)

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
| `content/05-examples.xml` | medium | One worked example end-to-end (filled artefact) | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-trust-boundary-diff-helper` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | JSON instance matching the output contract |
| `templates/skeleton.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trust-boundary-diff-helper.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[stride-lite-checklist-for-architects]]
- [[threat-model-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
