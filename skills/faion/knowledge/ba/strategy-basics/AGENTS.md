# Strategy Basics

## Summary

**One-sentence:** Produces a glossary + decision-tree primer that grounds BA team vocabulary (mission, vision, OKR, SMART, strategy vs tactics) before any strategic artefact is authored.

**One-paragraph:** Produces a glossary + decision-tree primer that grounds BA team vocabulary (mission, vision, OKR, SMART, strategy vs tactics) before any strategic artefact is authored. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Onboarding нових BA'ів — потрібен shared vocabulary перед strategy-analysis.
- BA-sponsor disagreement про що таке 'strategy' — треба joint primer.
- Pre-strategy-analysis warm-up — щоб не плутати mission/vision/OKR/SMART.
- Внутрішня CoP — щоквартальне оновлення термінології.

## Applies If (ALL must hold)

- BA team has new members lacking shared strategy vocabulary.
- Sponsor / BA disagree on what 'strategy' means.
- Engagement is about to use strategy-analysis or strategy-methods and needs grounded terms.
- Internal CoP wants a shared primer.

## Skip If (ANY kills it)

- Team is mature and vocabulary alignment is solved.
- Mid-execution sprint — no time for primer.
- Engagement is purely tactical with no strategic framing.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source materials (Porter, Mintzberg, Christensen) | URL list / library | BA team |
| Internal glossary draft (if any) | Markdown | BA team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[strategy-analysis]] | primer is its prerequisite warm-up |
| [[strategy-methods]] | method selection assumes shared vocabulary |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `collect-terms` | haiku | Mechanical extraction from source materials. |
| `write-glossary` | sonnet | Light judgement on phrasing + canonical definitions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/strategy-glossary.md` | Glossary template with term + canonical-def + example + anti-example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strategy-basics.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[strategy-analysis]]
- [[strategy-methods]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
