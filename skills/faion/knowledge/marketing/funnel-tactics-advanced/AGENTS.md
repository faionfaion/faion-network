# Funnel Tactics Advanced

## Summary

**One-sentence:** Industry-specific drop-off benchmarks, personalization by segment, exit-intent recovery, retargeting sequences, ICE-scored test prioritization and event-tracking patterns — for teams past basics who need second-order leverage.

**One-paragraph:** Industry-specific drop-off benchmarks, personalization by segment, exit-intent recovery, retargeting sequences, ICE-scored test prioritization and event-tracking patterns — for teams past basics who need second-order leverage. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Team has applied funnel-basics-framework already (mapped, measured, ICE-scored).
- Team has ≥ 1000 weekly users per funnel step (sample enough for segment splits).
- Team has paid-acquisition budget supporting retargeting sequences.

## Skip If (ANY kills it)

- Funnel-basics hasn't been applied — start there first.
- Sample too small for segmentation (< 500/segment) — collapse segments before applying advanced tactics.
- No retargeting infrastructure — apply post-click email basics before paid retargeting layers.

**Ефективно для:**

- Growth teams що мають baseline funnel-discipline і шукають next-leverage tactics.
- CRO managers що пишуть першу personalization strategy за segment / behaviour.
- Команди з retargeting bandwidth і need-for-discipline (post-click sequences).
- Аудит-ready середовища з вимогою event-tracking patterns evidence.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/conversion-optimizer` | Parent CRO context — funnel + activation discipline. |
| `pro/marketing/growth-marketer` | Adjacent metric / experimentation context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-funnel-tactics-advanced.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[funnel-basics-framework]]
- [[funnel-tactics-basics]]
- [[growth-conversion-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
