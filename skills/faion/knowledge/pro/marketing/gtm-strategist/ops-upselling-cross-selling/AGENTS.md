---
slug: ops-upselling-cross-selling
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Expansion-revenue playbook-step: detect usage triggers (80% of limit, advanced feature, team growth), match trigger to upgrade offer framed on the customer's own data point, one-click upgrade with proration, monthly NRR tracking.
content_id: "f095278ba1d235e1"
complexity: medium
produces: playbook-step
est_tokens: 4200
tags: ["upselling", "cross-selling", "expansion-revenue", "customer-success", "pricing-strategy"]
---
# Upselling and Cross-Selling

## Summary

**One-sentence:** Expansion-revenue playbook-step: detect usage triggers (80% of limit, advanced feature, team growth), match trigger to upgrade offer framed on the customer's own data point, one-click upgrade with proration, monthly NRR tracking.

**One-paragraph:** Upselling and Cross-Selling pins the discipline that turns this workflow from tribal knowledge into a reviewable, owned, version-controlled operating artefact. The methodology constrains input shape, output shape, evidence anchors, and named ownership; the JSON Schema in `content/02-output-contract.xml` drives a stdlib validator at commit time. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without a named owner are tagged stale. The artefact lives in the team's versioned space and is refreshed on a stated cadence.

## Applies If (ALL must hold)

- The team operates the system the methodology targets (`ops-upselling-cross-selling` scope).
- A named human owner is available to sign the artefact.
- The artefact lives in a version-controlled or wiki-style space with diff history.
- Tier ≥ pro (gated by tier-manifest).

## Skip If (ANY kills it)

- One-shot work with no recurrence — write a single doc, not a versioned artefact.
- A regulator or contract mandates a different shape — use the mandated template.
- No named owner is available — anonymous artefacts rot; defer until ownership resolved.

**Ефективно для:**

- Тригер-базованої експансії: 80% of limit / advanced feature use / team growth.
- Месіджу, framed на customer's own data point ('900 з 1000 subscribers').
- One-click upgrade з proration замість manual sales motion.
- Місячного NRR моніторингу як головного метрика експансії.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workflow spec | Markdown | team |
| Named owner | Person + role | team / RACI |
| Versioned space for artefact | Git / wiki with history | team |
| Trigger event | Event / threshold / schedule | operating cadence |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist` | Parent skill — provides go-to-market operating context for this methodology. |
| `pro/marketing/growth-marketer` | Peer skill — supplies adjacent growth-marketing methodology that may consume or produce inputs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source; includes skip-this-methodology guard | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: pick correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/ops-upselling-cross-selling.md` | Working skeleton for the `ops-upselling-cross-selling` artefact with required fields and `not_applicable: <reason>` markers per row. |
| `templates/_smoke-test.md` | Minimum viable filled artefact used by the validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ops-upselling-cross-selling.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only; supports `--help` and `--self-test`. | CI on artefact change; pre-commit. |

## Related

- [[gtm-strategist]]
- [[growth-marketer]]
- [[ops-pricing-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, owner presence, trigger naming, evidence presence) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
