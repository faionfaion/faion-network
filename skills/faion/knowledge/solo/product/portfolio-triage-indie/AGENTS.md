---
slug: portfolio-triage-indie
tier: solo
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a versioned triage report (per-product verdict + evidence + next-action) so a weekly portfolio metric scan stops being folklore and becomes a reviewable operating tool."
content_id: "78eede2be162d89c"
complexity: light
produces: report
est_tokens: 3500
tags: [product, solo, portfolio, triage, indie]
---

# Portfolio Triage Indie

## Summary

**One-sentence:** Produces a versioned triage report (per-product verdict + evidence + next-action) so a weekly portfolio metric scan stops being folklore and becomes a reviewable operating tool.

**Ефективно для:** Solopreneurs running 3-8 side projects who scan dashboards weekly but never commit a verdict or next-action, so the same triage decisions get re-litigated every week.

**One-paragraph:** An indie hacker scans portfolio metrics weekly but the scan never produces an artefact — verdicts evaporate, next-actions get re-derived from scratch the following week. This methodology produces a committed triage report: one row per product with a verdict (build / grow / maintain / sunset), the evidence link, and the next-action attached. Reviewed against outcomes at the next iteration. Output is consumed by the multi-product-portfolio-management config + the founder's calendar.

## Applies If (ALL must hold)

- Operator runs ≥3 products and scans metrics on a weekly cadence.
- Operator owns the artefact (or escalates ownership to a named role).
- A version-controlled or wiki-style space hosts the report.
- The scan trigger fires at a published cadence (calendar slot).

## Skip If (ANY kills it)

- One-shot work with no recurrence — write a single doc, not a versioned report.
- Operator runs <3 instances per year — review cadence costs more than it returns.
- Regulated context that mandates a different shape — use regulator's template instead.
- No named owner — defer until ownership is resolved; an anonymous report rots.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| product list | array | operator |
| MRR + traffic per product | object | Stripe + Plausible |
| knowledge-space URL | URL | operator |
| named owner | string | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/multi-product-portfolio-management` | Downstream — portfolio config consumes verdicts. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `scaffold-artefact` | haiku | Template fill from header + per-product rows; low cost. |
| `populate-evidence-fields` | sonnet | Per-row judgement: select correct evidence link, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: did the verdicts change behaviour? |

## Templates

| File | Purpose |
|---|---|
| `templates/portfolio-triage-indie.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/portfolio-triage-indie.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-portfolio-triage-indie.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[multi-product-portfolio-management]] — related methodology.
- [[kill-or-keep-criteria]] — related methodology.
- [[kill-criteria-template]] — related methodology.
- [[metric-deviation-hypothesis-framework]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
