---
slug: pm-tools-overview
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Overview report mapping team needs to the PM-tool market: MoSCoW requirements (Must/Should/Could/Won't), candidate list, fit-gap analysis, shortlist recommendation."
content_id: "1be2b3ebcbb17209"
complexity: medium
produces: report
est_tokens: 4400
tags: [pm-tools, tool-selection, moscow, requirements, adr]
---
# PM Tools Overview

## Summary

**One-sentence:** Overview report mapping team needs to the PM-tool market: MoSCoW requirements (Must/Should/Could/Won't), candidate list, fit-gap analysis, shortlist recommendation.

**One-paragraph:** PM Tools Overview defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Teams that do NOT yet have a PM tool and need a structured first selection.
- Coaches helping a portfolio map vague pain points into hard requirements before tool selection.
- Procurement / PMO that needs a fit-gap before triggering a deeper comparison (see pm-tools-comparison).
- Solopreneurs choosing their first tracker beyond a spreadsheet.

## Applies If (ALL must hold)

- Team can articulate 5-15 needs that a PM tool would address.
- At least one stakeholder can prioritise needs via MoSCoW.
- Time-box of 4-8h is available to compile the overview.
- Market scan can include 3-10 candidates without analysis paralysis.

## Skip If (ANY kills it)

- Team already has a working tool and only minor friction — patch the tool, don't re-select.
- Team has not done discovery on needs — overview without needs is shopping.
- Mandatory tool dictated by parent org or customer — write a single-choice ADR instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/05-examples.xml` | essential | One end-to-end worked example with trace | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pm-tools-overview_template_fill` | haiku | Bounded template fill, no judgement. |
| `pm-tools-overview_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `pm-tools-overview_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the PM tools overview report artefact. |
| `templates/requirements-doc.md` | Markdown skeleton for the MoSCoW requirements table. |
| `templates/poc-runner.py` | Reference script to scaffold PoC plans per shortlisted tool. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pm-tools-overview.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.
