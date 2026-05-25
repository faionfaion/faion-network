# CR / BUG Tracking

## Summary

**One-sentence:** Two lightweight side-streams that live alongside features — `crs/` for change requests, `bugs/` for defects — with simpler lifecycles than a full feature, global per-repo numbering, and explicit linkage to features when relevant.

**One-paragraph:** Not every change is a feature. CRs are small mutations to existing behaviour or contract; BUGs are defects against current behaviour. Both ship as one-page Markdown under `crs/{todo,done}/` or `bugs/{todo,in-progress,done}/`. Numbering is global per-repo with separate counters. Commit prefixes diverge from feature commits: `cr(CR0NN): ...` and `fix(BUG0NN): ...`. A BUG that exposes a missing business rule MUST update `project-spec/business-rules.md` in the same PR.

**Ефективно для:**

- Solo dev who needs the audit trail of an SDD feature without the spec/plan/tasks ceremony.
- Teams maintaining a public CHANGELOG where CR / BUG / FEATURE roll up cleanly.
- Connecting a BUG back to the spec gap that caused it.

## Applies If (ALL must hold)

- The change is too small to be a feature (no plan.md, no task breakdown).
- The SDD lifecycle is already in use for features.
- The repo has a clear answer to "what is the canonical numbering store?" (`crs/`, `bugs/`).

## Skip If (ANY kills it)

- Change affects multiple subsystems or requires a task breakdown → file as a feature instead.
- One-line documentation tweak → straight commit, no CR.

## Content

| File | What's inside |
|------|---------------|
| `content/01-cr-flow.xml` | CR shape (why, what changes, optional `linked-feature`), lifecycle `todo → done`, commit format `cr(CR0NN): ...`. |
| `content/02-bug-flow.xml` | BUG shape (symptom, repro, root cause, fix, regression test), lifecycle `todo → in-progress → done`, commit format `fix(BUG0NN): ...`. |
| `content/03-numbering.xml` | Global per-repo numbering; separate CR and BUG counters; how to allocate the next number. |
| `content/04-feature-linkage.xml` | Optional `linked-feature: F0NN` field; rule that BUG exposing missing business rule MUST update business-rules.md same PR. |

## Related

- [[sdd-workflow-overview]] — CR / BUG side-streams parallel the feature lifecycle.
- [[project-spec-structure]] — BUG-driven business-rule updates land here.
- [[readiness-checklist]] — does NOT apply to CR / BUG; they have their own lighter gate.

## Decision tree

If the work is a defect against current behaviour → BUG. If it is a small mutation that needs a record but no task plan → CR. Otherwise route to feature.
