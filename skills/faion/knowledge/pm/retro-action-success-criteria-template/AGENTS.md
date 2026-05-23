# Retro Action Success Criteria Template

## Summary

**One-sentence:** A retro action template that forces every action item to declare measurable success criteria (named input + measurement + numeric threshold + sprint deadline + owner role), so retros stop emitting "communicate better" and start emitting falsifiable experiments.

**One-paragraph:** Retros generate vague action items ("communicate better", "improve handoffs") because no methodology enforces a measurable result. This methodology pins the action shape: each item carries a named experiment, a named input metric (cycle-time, defect-escape, eNPS, etc.), a numeric threshold ("reduce p95 cycle from 4d to 3d"), a sprint deadline, and an owner role. Outcome review at the next retro confirms or rejects the experiment with evidence. Versioned + signed; quarterly review removes never-fired experiments and prunes dead actions.

**Ефективно для:**

- Bi-weekly retro with mistake-memory feedback in product-dev teams.
- Cross-team alignment via consistent action shape.
- Cross-sprint experiment tracking — pattern detection across retros.
- Quarterly review: which actions converted to outcomes, which were folklore.

## Applies If (ALL must hold)

- Team runs retros on a published bi-weekly or sprint-aligned cadence.
- Cycle-time / defect / morale signal is measurable.
- Team owns the artefact (or escalates to named role).
- ≥ 6 retros / quarter so trend data is meaningful.

## Skip If (ANY kills it)

- Single-cycle or ad-hoc retro — methodology overhead exceeds value.
- < 3 retros per year — bespoke notes cheaper than rule-driven.
- Regulated context with mandated retro format — adopt that template.
- No named owner.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Last N retro action lists | Markdown / Jira | retro tool |
| Cycle-time / defect / morale telemetry | exports | platform |
| Stakeholder register (for owner roles) | YAML | HR |
| Last quarter outcome data | JSON | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[team-development]] | Retro themes feed Tuckman staging + skill matrix. |
| [[value-stream-management]] | Cycle-time + DORA metrics feed action thresholds. |
| [[team-morale-pulse-survey]] | Morale signal feeds emotional-axis actions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: fixed shape, evidence fields, version + owner, fill budget, reuse marker | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `RetroActionItem` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: cargo-cult, ownership ambiguity, drift, leakage, no outcome review, trigger drift | ~900 |
| `content/04-procedure.xml` | medium | 5-step: scaffold → write actions → measure → outcome review → quarterly synth | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: measurable threshold? owner role? deadline? → accept / repair / archive | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-action` | haiku | Mechanical fill. |
| `derive-threshold` | sonnet | Per-signal judgment on numeric threshold. |
| `outcome-review` | sonnet | Pre-vs-post comparison with evidence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | RetroActionItem skeleton |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum viable filled `RetroActionItem` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-retro-action-success-criteria-template.py` | Validate: numeric threshold, owner role, sprint deadline, measurement source | Pre-merge |
| `scripts/staleness-check.py` | Flag templates whose `last_reviewed` > 90 days | Weekly cron |

## Related

- [[team-development]]
- [[value-stream-management]]
- [[team-morale-pulse-survey]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates an action item on (a) numeric threshold present, (b) owner role named, (c) deadline sprint-bounded, (d) measurement source available. Every leaf references a rule from `01-core-rules.xml`.
