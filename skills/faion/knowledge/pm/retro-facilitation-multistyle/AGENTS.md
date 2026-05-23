# Retro Facilitation Multistyle

## Summary

**One-sentence:** Five canonical retro formats (mad-sad-glad, 4Ls, sailboat, lean-coffee, anonymous-async) with named selection criteria per team state, plus an evidence-anchored outcome review so retros stop being folklore.

**One-paragraph:** scrum-ceremonies mentions retros generically; there is no facilitation playbook with multiple formats and selection criteria. Async cross-timezone teams (P4 outsource) need anonymous-async; stable product teams (P6) cycle formats to avoid fatigue. This methodology pins the artefact: a versioned per-retro instance with the chosen format, the selection rationale (team-state evidence), the action items it produced, the named owner of those actions, and the outcome review at the next retro that closes the loop on whether actions changed behaviour.

**Ефективно для:**

- Solo PM facilitating retros across an async/outsourced team.
- Stable product team cycling formats to avoid retro fatigue (≥3 instances/year).
- Documenting why a format was picked + whether it produced change.
- Replacing free-form retro notes with a reviewable artefact.

## Applies If (ALL must hold)

- PM facilitates retros on a recurring cadence (≥3 per year).
- PM owns the artefact (or escalates ownership to a named role).
- Team uses a version-controlled or wiki-style space for retro notes.
- The retro trigger fires on a published cadence (event, threshold, schedule).

## Skip If (ANY kills it)

- One-shot retro with no recurrence — write a single doc.
- Team has &lt; 3 retros per year — review cadence costs more than it returns.
- Regulated context mandating a different shape — use the regulator's template.
- No named owner — defer until ownership is resolved.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Access to repo / wiki hosting retro notes | repo path | platform |
| Named owner for retro outcomes | identity | PM |
| List of 5 supported formats with their selection criteria | doc | PM |
| Outcome-review cadence published | calendar | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[retro-format-rotation-guide]] | Sibling guide that informs format choice across multiple retros. |
| [[status-report-templates-by-audience]] | Retro outputs flow into status reports. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules — explicit trigger, bounded output, evidence-anchored, named owner, iteration loop | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for retro instance + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 6 known failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `format_selection` | sonnet | Team-state judgement (async vs in-person, fatigue cycle). |
| `retro_facilitation_notes` | sonnet | Per-instance synthesis of team input. |
| `outcome_review_synthesis` | opus | Cross-cycle: did action items change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/retro-instance.md` | Per-retro instance template (format / actions / owner / review) |
| `templates/format-card.md` | One-pager listing the 5 supported formats + selection criteria |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-retro-facilitation-multistyle.py` | Validate retro instance against 02-output-contract schema | Pre-merge + next retro review |

## Related

- [[retro-format-rotation-guide]]
- [[status-report-templates-by-audience]]
- [[solo-burnout-tripwires]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by team state, format choice, action-item evidence, owner naming, and outcome-review staleness onto a rule from `content/01-core-rules.xml`. Walk it before every retro.
