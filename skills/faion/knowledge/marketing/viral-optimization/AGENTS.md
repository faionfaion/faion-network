# Viral Loop Optimization

## Summary

**One-sentence:** Sequenced viral-loop optimization: decompose K into i + c, fix c first (invite landing), then i (share moments), one variable per A/B test, retention-adjusted decisions.

**One-paragraph:** Sequenced viral-loop optimization: decompose K into i + c, fix c first (invite landing), then i (share moments), one variable per A/B test, retention-adjusted decisions. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Teams з измеренним baseline K-factor що готові інвестувати в optimization.
- Перед запитом resources на share-moment redesign — спершу confirm c is bottleneck.
- Якщо K plateaued > 4 weeks — це cue для systematic optimization sweep.
- Перед re-platforming viral loop infrastructure — pick wins першими.

## Applies If (ALL must hold)

- viral-metrics уже implemented — K, i, c, K_eff measured weekly.
- Baseline K stable >= 4 weeks (not still decaying from launch).
- Engineering + experimentation capacity for >= 4 A/B tests per quarter.

## Skip If (ANY kills it)

- K-factor < 0.05 — це archetype problem, не optimization. Run viral-loops first.
- Retention < threshold for archetype — optimize retention before viral.
- Loop < 4 weeks old — не stable enough baseline для optimization.

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
| `pro/marketing/growth-marketer` | Parent role context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-tradeoffs` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/playbook-step-skeleton.md` | Viral Loop Optimization skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Viral Loop Optimization. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-viral-optimization.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[viral-loops]]
- [[viral-metrics]]
- [[growth-experiment-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
