---
slug: agency-discovery-call-playbook
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a 45-minute discovery-call playbook output: budget range, decision-maker, fit score, and next-step recommendation with verbatim quotes.
content_id: "b747071d6b799df6"
complexity: medium
produces: report
est_tokens: 4300
tags: [agency, ba, discovery, sales, playbook]
---
# Agency Discovery Call Playbook

## Summary

**One-sentence:** Produces a 45-minute discovery-call playbook output: budget range, decision-maker, fit score, and next-step recommendation with verbatim quotes.

**One-paragraph:** Produces a 45-minute discovery-call playbook output: budget range, decision-maker, fit score, and next-step recommendation with verbatim quotes. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Agency-founder running new-client discovery — потрібен 45-min structured script.
- Inbound lead screening: budget + decision-maker + fit за 45 хвилин.
- Sales-discovery (не BA-discovery), де потрібен sales-shaped playbook.
- Post-call writeup для proposal author — кваліфікований handoff.

## Applies If (ALL must hold)

- Agency founder running new-client discovery calls and needing repeatable structure.
- Inbound lead screening where 45 minutes must yield budget / decision-maker / fit.
- Sales-discovery vs BA-discovery confusion — sales context needs sales-shaped playbook.
- Post-call writeup that downstream proposal author consumes.

## Skip If (ANY kills it)

- Existing client where discovery is replaced by account management.
- Pure inbound where lead has filled a detailed form covering budget + decision-maker.
- Pre-discovery rapport call (no scope context yet).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Lead intake data (form / referral note) | CRM record | sales ops |
| Service-line catalogue | Markdown | agency partners |
| Pricing range table | Markdown / spreadsheet | agency partners |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[elicitation-techniques]] | interview technique base |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `prep-call` | haiku | Mechanical assembly of lead intake + service catalogue. |
| `run-call-script` | sonnet | Apply script branches against state. |
| `writeup-findings` | opus | Synthesise narrative + recommendation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/discovery-call-script.md` | 45-min call script with 4 phases. |
| `templates/post-call-writeup.md` | Writeup template: budget, decision-maker, fit, next step. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-discovery-call-playbook.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[elicitation-techniques]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
