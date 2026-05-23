---
slug: strategy-methods
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a method-selection record (Porter Five Forces / SWOT / Wardley / OST / Blue Ocean) with explicit fit criteria, scoring, and limitation register.
content_id: "220e37cbffb6bd8f"
complexity: medium
produces: decision-record
est_tokens: 3600
tags: [ba, strategy, method, porter, wardley]
---
# Strategy Methods

## Summary

**One-sentence:** Produces a method-selection record (Porter Five Forces / SWOT / Wardley / OST / Blue Ocean) with explicit fit criteria, scoring, and limitation register.

**One-paragraph:** Produces a method-selection record (Porter Five Forces / SWOT / Wardley / OST / Blue Ocean) with explicit fit criteria, scoring, and limitation register. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Strategy analysis у процесі — треба свідомо вибрати method, а не за замовчуванням SWOT.
- Stakeholder disagreement — competing methods (Porter vs Wardley) треба порівняти.
- Multi-unit program — різні методи для різних BU.
- Audit застарілого strategy artefact — треба зрозуміти яким методом він зроблений.

## Applies If (ALL must hold)

- Strategy analysis is underway and a method must be chosen.
- Stakeholder disagreement on framing — methods compete.
- Multi-context program needing different methods per business unit.
- Reviewing a stale strategy artefact for which the method is unclear.

## Skip If (ANY kills it)

- Strategy method is already mandated.
- Tactical scope where method selection adds no value.
- All candidate methods are equally weak — bigger problem exists upstream.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Strategic context (industry, maturity, competition) | Markdown | BA / PM |
| Available data (financials, market intel) | CSV / dashboard | data team |
| Stakeholder availability for the chosen method | calendar | BA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[strategy-basics]] | shared vocabulary prereq |
| [[strategy-analysis]] | downstream consumer of the chosen method |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-context` | haiku | Mechanical fit-scoring per method axis. |
| `recommend-method` | opus | Synthesise method recommendation under contradicting signals. |
| `draft-limitation-register` | sonnet | List known weaknesses + mitigations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scoring-matrix.md` | Method scoring matrix with fit axes. |
| `templates/limitation-register.md` | Per-method limitation register. |
| `templates/sensitivity.py` | Stdlib sensitivity analysis for method-selection scores. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strategy-methods.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[strategy-basics]]
- [[strategy-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
