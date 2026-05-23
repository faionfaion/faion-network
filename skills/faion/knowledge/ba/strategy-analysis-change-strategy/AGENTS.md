# Strategy Analysis — Change Strategy

## Summary

**One-sentence:** A sequenced plan from current to future state listing solution options, transition states, readiness gaps, and the recommended path with cost-risk-time trade-offs.

**One-paragraph:** Once business need + current + future state are clear, the question becomes 'how do we get there?'. This methodology produces a change-strategy spec with: ≥2 solution options, transition states between current and future, organisational-readiness gaps, cost-risk-time trade-offs per option, and a recommendation. The artefact feeds requirements work and the steering committee approval.

**Ефективно для:**

- Multi-quarter transformation programs (ERP, CRM, data-platform).
- Make-vs-buy decisions at program inception.
- Re-platforming initiatives with active production users.
- Steering-committee approval gates demanding option comparison.

## Applies If (ALL must hold)

- business-need + current-state + future-state specs exist
- ≥2 viable solution options can be articulated
- named decision-maker / steering committee exists
- the engagement is large enough that 'just start building' is too risky (≥3 months)

## Skip If (ANY kills it)

- current + future state specs missing — produce them first
- single forced solution (regulatory mandate, vendor lock-in) — skip option comparison
- the engagement is small enough that option analysis costs more than it saves

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| business-need spec | MD / wiki | strategy-analysis-business-need |
| current-state spec | MD / wiki | strategy-analysis-current-state |
| future-state spec | MD / wiki | strategy-analysis-future-state |
| budget envelope + timeline window | wiki | sponsor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[strategy-analysis-business-need]] | Defines why the change is needed. |
| [[strategy-analysis-current-state]] | Defines the starting point of the transition. |
| [[strategy-analysis-future-state]] | Defines the target end-state. |
| [[strategy-analysis-gap-analysis]] | Defines the gap the strategy must close. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: ≥2 options, named transition states, readiness gap per option, cost-risk-time trade-off, named decision-maker | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for change-strategy spec: options, transitions, readiness, recommendation | 800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: single-option theatre, ignored readiness, missing transition states, decision-maker absent, recommendation without rationale | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: enumerate options → define transitions → assess readiness → score trade-offs → recommend | 700 |
| `content/05-examples.xml` | essential | Worked example: data-platform re-platforming with 3 options + recommendation | 500 |
| `content/06-decision-tree.xml` | essential | Tree on gap size + budget + risk tolerance | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `enumerate_options` | sonnet | Generate ≥2 distinct viable options. |
| `readiness_gap_check` | sonnet | Per-option organisational-readiness assessment. |
| `trade_off_score` | sonnet | Cost-risk-time scoring per option. |
| `recommendation_narrative` | opus | High-stakes synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/change-strategy-spec.md` | Markdown skeleton with options + transitions + readiness + recommendation. |
| `templates/option-trade-off.csv` | Header for option × dimension scoring matrix. |
| `templates/_smoke-test.md` | Minimum viable change strategy. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strategy-analysis-change-strategy.py` | Validates change-strategy spec against the JSON Schema. | Before steering-committee review; pre-commit. |

## Related

- [[strategy-analysis-business-need]]
- [[strategy-analysis-current-state]]
- [[strategy-analysis-future-state]]
- [[strategy-analysis-gap-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
