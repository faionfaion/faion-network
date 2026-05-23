# RACI AI Assisted

## Summary

**One-sentence:** AI-assisted RACI matrix builder: ingests project charter + WBS + team roster, emits a typed `RACIMatrix` with exactly-one A per row, flags orphaned R's and duplicate A's, and refreshes when the roster changes.

**One-paragraph:** The corpus covers RACI as a static doc but not the methodology that drafts, validates, and refreshes one. Without the loop, RACI rots within 4 weeks of project start. This methodology pins it: trigger fires on (a) project kickoff, (b) roster change, (c) quarterly review. Output is a typed `RACIMatrix` mapping each WBS-leaf id to {responsible[], accountable, consulted[], informed[]} with named-owner discipline, exactly one A per row, and evidence anchor per assignment (charter line, WBS dictionary entry, or stakeholder register row). Refreshed on roster delta; quarterly review removes orphaned entries.

**Ефективно для:**

- Multi-team coordination & dependency-graph reasoning (P6-product context).
- Roster onboarding / offboarding triggering RACI delta.
- Audit: every WBS leaf has exactly one accountable role.
- Quarterly review removing dead rows + flagging duplicates.

## Applies If (ALL must hold)

- A WBS spec exists (see [[wbs-creation]]) — RACI binds to WBS-leaf ids.
- A stakeholder register exists with role + person fields.
- Project manager owns the artefact (or escalates to named role).
- Trigger event fires at a published cadence (kickoff / roster delta / quarterly).

## Skip If (ANY kills it)

- One-shot project with no recurrence — single doc, not a versioned artefact.
- < 3 RACI cycles per year — review cadence costs more than it returns.
- Regulated context mandating a specific accountability format — adopt that template.
- No named owner — defer until ownership resolved.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Project charter | Markdown | sponsor |
| WBS spec | JSON | [[wbs-creation]] |
| Team roster | YAML | HR / stakeholder register |
| Last RACI delta | JSON | this methodology (prior cycle) |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[wbs-creation]] | RACI rows reference WBS-leaf ids. |
| [[team-development]] | Skills matrix informs viable role assignments. |
| [[proposal-red-team-checklist]] | RACI inconsistencies surface during proposal red-team. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: explicit trigger, bounded output, evidence-anchored, named owner, iteration loop | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `RACIMatrix` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: cargo-cult, ownership ambiguity, drift, example-text leakage, no outcome review, trigger drift | ~900 |
| `content/04-procedure.xml` | medium | 5-step: scaffold → assign → validate → publish → quarterly-review | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: trigger present? owner named? evidence? per-row A count? → action + rule | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `raci-scaffold` | haiku | Mechanical fill from WBS rows + roster. |
| `raci-assign-A` | sonnet | Per-row judgment on the single accountable role. |
| `raci-validate` | haiku | Mechanical exactly-one-A + orphaned-R check. |
| `outcome-review-synthesis` | opus | Cross-quarter synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | RACI matrix skeleton with not_applicable markers |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum-viable filled `RACIMatrix` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-raci-ai-assisted.py` | Validate `RACIMatrix`: exactly-one-A, evidence anchors, owner | Pre-merge |
| `scripts/staleness-check.py` | Flag matrices whose `last_reviewed` exceeds 90 days | Weekly cron |

## Related

- [[wbs-creation]]
- [[team-development]]
- [[proposal-red-team-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (trigger fired, owner named, A-count per row, evidence presence, staleness) to run / suppress / repair-A / refresh. Every leaf references a rule from `01-core-rules.xml`.
