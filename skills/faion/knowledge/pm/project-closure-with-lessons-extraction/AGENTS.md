# Project Closure with Lessons Extraction

## Summary

**One-sentence:** Pinned closure method for distressed-project rescues — outcome-vs-charter variance, behavioural-change lessons with named owners, follow-up items, and reviewable artefact at the next iteration.

**One-paragraph:** Project closure usually devolves into bullet-point lessons that nobody implements. This methodology pins the artefact: a structured closure report with outcome-vs-charter variance, lessons phrased as behaviour changes (not generalities), named owners per lesson, target adoption dates, and explicit decisions for the next project. The closure report is reviewed at the start of the next project to verify lessons were carried forward. Designed primarily for distressed-project (90-day turnaround) closures but generalises to any closure.

**Ефективно для:**

- Distressed-project turnarounds where lessons must change behaviour next time.
- Programme closures with multi-stakeholder learning to capture.
- Regulated programmes requiring documented closure evidence.
- Outsource delivery closures feeding warranty-runbook construction.

## Applies If (ALL must hold)

- Project is closing (delivered, partially delivered, or abandoned).
- Charter exists for outcome-vs-charter comparison.
- Team is available for closure interviews.
- There is a follow-on project where lessons can be applied.

## Skip If (ANY kills it)

- Project is mid-flight and closure was triggered prematurely — pause and reassess.
- No follow-on context exists; lessons would die in the report.
- Team disbanded before closure — captured lessons risk being orphaned.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Charter | signed PDF / MD | sponsor |
| Final deliverables list | MD / CSV | delivery |
| Outcomes data | metrics export | analytics |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `stakeholder-register` | Interview list draws on register. |
| `risk-register` | Closed risks feed lessons. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — outcome-vs-charter, behaviour-change lessons, named owner per lesson, target adoption date, next-project review | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the closure report | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: kick-off → gather → interview → synthesise → publish → carry-forward | 900 |
| `content/05-examples.xml` | optional | Worked closure report snippet for a distressed-project rescue | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping report state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `interview-script` | haiku | Template fill from team list. |
| `lesson-synthesis` | opus | Translates anecdotes into behaviour changes — high-leverage. |
| `carry-forward-check` | sonnet | Cross-project applicability assessment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/closure-report.md` | Closure report skeleton with lesson table + decisions. |
| `templates/lessons-interview.md` | Per-role lessons interview script. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-project-closure-with-lessons-extraction.py` | Schema-validate the closure report. | Pre-publish + before next-project kick-off. |

## Related

- [[post-handover-warranty-runbook]]
- [[stakeholder-engagement]]
- [[risk-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the project-closure-with-lessons-extraction input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
