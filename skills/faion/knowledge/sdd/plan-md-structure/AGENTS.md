# plan.md Structure

## Summary

**One-sentence:** Per-feature `plan.md` merges what used to be `design.md` and `implementation-plan.md` into ONE file with two top-level sections — `## Design` and `## Execution Plan`.

**One-paragraph:** In observed practice (F021, F022, F002) the design doc and the implementation plan cross-referenced each other on every section, and splitting them produced drift between the two files. The merge collapses that into atomic updates: any decision change touches one file. Trivial features (≤3 tasks, no new contracts) may skip plan.md entirely; the spec.md task checklist is sufficient.

**Ефективно для:**

- Mid-size features where decisions and task breakdown depend on each other.
- Multi-task features that introduce a new internal contract or sequencing requirement.

## Applies If (ALL must hold)

- The feature has 4+ tasks OR introduces a new contract / schema / sequencing constraint.
- The feature folder is in `features/in-progress/` or `features/todo/`.
- The team agreed that this feature warrants more than spec.md + task list.

## Skip If (ANY kills it)

- Feature has ≤3 tasks AND introduces no new contract → spec.md task checklist is the plan.
- Documentation-only feature → no plan needed.
- Already shipping a CR / BUG → wrong lifecycle, use cr-bug-tracking.

## Content

| File | What's inside |
|------|---------------|
| `content/01-shape.xml` | The two-H2 structure. Design: package layout, feature-scoped API contracts, schemas, sequencing. Execution Plan: wave map, task table, dependencies, risks. |
| `content/02-when-to-skip.xml` | Concrete skip criteria for trivial features. |
| `content/03-rationale.xml` | Empirical anchor for the merge: F021/F022/F002 showed design.md and impl-plan.md cross-referencing every section, splitting caused drift. |

## Related

- [[sdd-workflow-overview]] — plan.md is the `plan` phase artefact.
- [[project-spec-structure]] — project-spec/ holds system-wide contracts; plan.md holds FEATURE-scoped contracts only.
- [[readiness-checklist]] — readiness gate verifies plan.md tasks are all done.

## Decision tree

If the feature is trivial (≤3 tasks, no new contracts) → skip plan.md. Otherwise produce plan.md with two H2 sections.
