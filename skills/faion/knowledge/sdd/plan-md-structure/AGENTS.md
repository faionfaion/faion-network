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

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules: two H2s mandatory, Design contents, Execution Plan contents, skip when ≤3 tasks and no new contract, when in doubt write, single file only, split by sub-section not file, in-file anchors | ~1250 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for plan.md (Design + Execution Plan with `T0N` tasks) or a justified trivial skip; valid / invalid examples; 6 forbidden patterns | ~1950 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: F021 two-file drift, splitting back "because long", skipping a non-trivial feature, tasks without ids / deps | ~900 |
| `content/04-procedure.xml` | essential | 5 steps: trivial test, write Design, write Execution Plan, in-file cross-references, keep it one file | ~1050 |
| `content/05-examples.xml` | recommended | Execution Plan waves + task table, phone-field skip (good) vs Stripe webhook skip (bad), the F021 / F022 / F002 merge rationale, what we keep / drop | ~750 |
| `content/06-decision-tree.xml` | essential | Feature lifecycle gate, then ≤3 tasks and no new contract → skip; 4+ or new contract → plan.md; unsure → write; two files → merge | ~600 |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-plan-md-structure.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[sdd-workflow-overview]] — plan.md is the `plan` phase artefact.
- [[project-spec-structure]] — project-spec/ holds system-wide contracts; plan.md holds FEATURE-scoped contracts only.
- [[readiness-checklist]] — readiness gate verifies plan.md tasks are all done.

## Decision tree

If the feature is trivial (≤3 tasks, no new contracts) → skip plan.md. Otherwise produce plan.md with two H2 sections.
