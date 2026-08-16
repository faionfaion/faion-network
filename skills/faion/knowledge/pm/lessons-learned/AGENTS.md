# Lessons Learned

## Summary

**One-sentence:** Continuous knowledge-capture: in-flight observation log + per-milestone retro + post-mortem report, feeding a project-wide knowledge base and triggering SOP updates.

**One-paragraph:** Continuous knowledge-capture: in-flight observation log + per-milestone retro + post-mortem report, feeding a project-wide knowledge base and triggering SOP updates.

**Ефективно для:**

- PMO, що хоче перетворити кожен проект на institutional learning.
- Agency, що оптимізує delivery rate cards за результатами retros.
- Регульованих програм, де post-mortem — частина audit trail.
- Команд, що страждають від repeating mistakes без формального learning loop.

## Applies If (ALL must hold)

- Project has at least one milestone with measurable outcome.
- Team can dedicate 2-3 hours for retro per milestone.
- Project will repeat or have peers in the portfolio.
- PM is willing to publish post-mortem cross-team.

## Skip If (ANY kills it)

- One-shot project with no peers in portfolio.
- Team explicitly outsources retros to an external coach.
- &lt;1-month project — overhead exceeds benefit.
- No psychological-safety for blameless post-mortem.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[communications-management]] | Comms plan determines who reads the report. |
| [[delivery-sop-template]] | SOPs updated when lessons trigger procedural change. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + `skip-this-methodology` | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | one worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `observation-log-keeper` | haiku | Append observation rows in-flight. |
| `retro-facilitator` | sonnet | Synthesize retro themes from observation log + survey. |
| `post-mortem-author` | opus | Author blameless post-mortem report. |
| `sop-updater` | sonnet | Translate lesson into SOP change. |

## Templates

| File | Purpose |
|------|---------|
| `templates/observation-log.md.j2` | In-flight observation row: date, observer, signal, hypothesis. |
| `templates/observation-log.md` | In-flight observation row: date, observer, signal, hypothesis. Generated from `templates/observation-log.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/retro-notes.md.j2` | Per-milestone retro: went-well, went-wrong, decisions, action items. |
| `templates/retro-notes.md` | Per-milestone retro: went-well, went-wrong, decisions, action items. Generated from `templates/retro-notes.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/post-mortem.md.j2` | Blameless post-mortem: timeline, root cause, contributing factors, actions. |
| `templates/post-mortem.md` | Blameless post-mortem: timeline, root cause, contributing factors, actions. Generated from `templates/post-mortem.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/lesson-record.md.j2` | Single lesson-learned record — situation, impact, 5-whys root cause, recommendation. |
| `templates/lesson-record.md` | Single lesson-learned record — situation, impact, 5-whys root cause, recommendation. Generated from `templates/lesson-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/session-agenda.md.j2` | Lessons-learned session agenda and facilitation script. |
| `templates/session-agenda.md` | Lessons-learned session agenda and facilitation script. Generated from `templates/session-agenda.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lessons-learned.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[delivery-sop-template]]
- [[communications-management]]
- [[change-control]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (milestone_count, peer_projects_in_portfolio, psychological_safety) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
