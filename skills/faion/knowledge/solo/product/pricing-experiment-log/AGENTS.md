---
slug: pricing-experiment-log
tier: solo
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a versioned pricing experiment log (hypothesis → toggle → window → result → decision per flip) so price changes stop being folklore and become a reviewable operating tool."
content_id: "7273e158cf845fc0"
complexity: light
produces: report
est_tokens: 2900
tags: [product, solo, pricing, experiment, log]
---

# Pricing Experiment Log

## Summary

**One-sentence:** Produces a versioned pricing experiment log (hypothesis → toggle → window → result → decision per flip) so price changes stop being folklore and become a reviewable operating tool.

**Ефективно для:** Solopreneurs A/B-flipping prices ad-hoc across a year without a log, then losing track of which flip caused which MRR change.

**One-paragraph:** Pricing-experiment playbooks exist but no living log/template tracks hypotheses → result → decision across a year of flips. This methodology produces a versioned log: one row per experiment with hypothesis (≥1 falsifiable claim), toggle (what changed), measurement window, observed result vs control, and decision (keep / revert / iterate). Output is consumed by the operator's pricing review + financial forecast.

## Applies If (ALL must hold)

- Operator runs ≥1 pricing experiment per quarter.
- Operator owns the artefact (or escalates ownership to a named role).
- A version-controlled or wiki-style space hosts the log.
- The toggle event fires at a published cadence (calendar slot, threshold, A/B platform).

## Skip If (ANY kills it)

- One-shot price test with no recurrence — write a single doc.
- Operator runs <3 experiments per year — log cadence costs more than it returns.
- Pricing is contractually locked — log has nothing to record.
- No named owner — defer until ownership resolved.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| hypothesis statement (falsifiable) | string | founder |
| toggle definition | string | operator |
| baseline MRR + conversion % | snapshot | Stripe |
| measurement window | datetime range | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/metric-deviation-hypothesis-framework` | Sibling — hypothesis discipline carries over. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `scaffold-artefact` | haiku | Template fill from header + per-experiment rows. |
| `populate-evidence-fields` | sonnet | Per-row judgement: select correct evidence link, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-experiment synthesis at quarterly review. |

## Templates

| File | Purpose |
|---|---|
| `templates/pricing-experiment-log.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/pricing-experiment-log.md` | Markdown skeleton with the required fields. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-pricing-experiment-log.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[metric-deviation-hypothesis-framework]] — related methodology.
- [[subscription-lifecycle-edge-cases]] — related methodology.
- [[vanity-metrics-audit]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
