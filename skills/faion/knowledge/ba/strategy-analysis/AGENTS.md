# Strategy Analysis

## Summary

**One-sentence:** Produces a business-need statement + gap analysis + change strategy tying current state to future state with measurable closure plan.

**One-paragraph:** Produces a business-need statement + gap analysis + change strategy tying current state to future state with measurable closure plan. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Pre-discovery: business need ще розмитий — потрібно його записати.
- Investment-justification — explicit current vs future state із вимірюваною різницею.
- Multi-year roadmap — baselined gap analysis для пріоритетів.
- Compliance/regulatory shift — change strategy документована.

## Applies If (ALL must hold)

- Strategic initiative entering pre-discovery — business need is fuzzy.
- Investment justification requires explicit current-vs-future state.
- Multi-year roadmap requires baselined gap analysis.
- Compliance / regulatory shift requires documented change strategy.

## Skip If (ANY kills it)

- Tactical scope where strategy analysis is overkill.
- Business need is already documented and current.
- Initiative is execution-phase, not framing-phase.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Executive context (strategic objectives, OKRs) | Markdown | exec sponsor |
| Current-state artefacts (process maps, KPIs) | Markdown / data | operations |
| Future-state aspiration | Markdown / brief | exec sponsor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[strategy-basics]] | vocabulary + OKR/SMART framing |
| [[strategy-methods]] | tactical methods slot below this artefact |

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
| `frame-business-need` | opus | Synthesise need under political pressure. |
| `compute-gap` | sonnet | Compare current vs future state across measurable axes. |
| `draft-change-strategy` | opus | Synthesise narrative with milestones + risks. |

## Templates

| File | Purpose |
|------|---------|
| `templates/business-need-statement.md` | BABOK KA6 business need statement skeleton. |
| `templates/gap-analysis.md` | Current-vs-future gap table with closure plan. |
| `templates/validate-ka6.sh` | Shell validator for BABOK KA6 artefacts. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strategy-analysis.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[strategy-basics]]
- [[strategy-methods]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
