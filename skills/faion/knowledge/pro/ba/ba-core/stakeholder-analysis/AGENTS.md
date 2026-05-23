---
slug: stakeholder-analysis
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a stakeholder register + power/interest map + RACI matrix mapping who decides, contributes, signs off, and must be informed across the engagement.
content_id: "eda0fba34696f138"
complexity: medium
produces: spec
est_tokens: 4300
tags: [ba, stakeholder, raci, power-interest, engagement]
---
# Stakeholder Analysis

## Summary

**One-sentence:** Produces a stakeholder register + power/interest map + RACI matrix mapping who decides, contributes, signs off, and must be informed across the engagement.

**One-paragraph:** Produces a stakeholder register + power/interest map + RACI matrix mapping who decides, contributes, signs off, and must be informed across the engagement. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- New engagement з >5 stakeholder'ів — треба чіткий RACI + power/interest map.
- Cross-functional/multi-vendor програма, де accountability розпливчатий.
- Conflict-heavy initiative — escalation paths мають бути названі заздалегідь.
- Compliance/audit context — sign-off chain документований.

## Applies If (ALL must hold)

- New engagement or initiative with >5 stakeholders.
- Cross-functional / multi-vendor program where accountability is unclear.
- Conflict-heavy context where escalation paths must be named.
- Compliance audit demanding documented sign-off chain.

## Skip If (ANY kills it)

- Solo / pair-team work with no external stakeholders.
- Stakeholder list is already maintained and current elsewhere.
- Initiative is too short (< 2 weeks) to justify register maintenance.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Org chart | CSV / HRIS export | people-ops |
| Engagement scope | Markdown / SOW | PM |
| Decision rights mandate | Output of ba-planning T3 | BA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ba-planning]] | T2 stakeholders feed into ba-planning bundle |

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
| `extract-stakeholders` | haiku | Mechanical extraction from org chart + scope. |
| `score-power-interest` | sonnet | Map each stakeholder onto power/interest grid. |
| `build-raci` | sonnet | Assign R/A/C/I per artefact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholder-register.md` | Master register: name, role, category, contact, influence, interest. |
| `templates/stakeholder-profile.md` | Per-key-stakeholder profile with engagement strategy. |
| `templates/raci-lint.sh` | Shell helper checking RACI has exactly one A per row. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-analysis.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[ba-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
