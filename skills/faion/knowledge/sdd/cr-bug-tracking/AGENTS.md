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

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 testable rules: CR one page / two states / `cr(CR0NN):`, BUG five sections / three states / `fix(BUG0NN):`, two global counters never reset, optional `linked-feature`, revealing BUG updates project-spec same PR | ~1400 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for a CR / BUG record with kind-conditional sections and states; valid / invalid examples; 6 forbidden patterns | ~1750 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: BUG closed without regression test, counter reset, "update spec sometime", oversized CR, CR in-progress state | ~950 |
| `content/04-procedure.xml` | essential | 6 steps: classify, allocate the next number, write the file, move through lifecycle, commit with prefix, update project-spec for a revealing BUG | ~1150 |
| `content/05-examples.xml` | recommended | CR042 and BUG019 files in full, commit subjects, the number-allocation one-liners, the BR-051 spec entry | ~800 |
| `content/06-decision-tree.xml` | essential | Defect? → reveals missing rule? → BUG with / without spec update; else CR, feature, or straight commit | ~650 |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cr-bug-tracking.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[sdd-workflow-overview]] — CR / BUG side-streams parallel the feature lifecycle.
- [[project-spec-structure]] — BUG-driven business-rule updates land here.
- [[readiness-checklist]] — does NOT apply to CR / BUG; they have their own lighter gate.

## Decision tree

If the work is a defect against current behaviour → BUG. If it is a small mutation that needs a record but no task plan → CR. Otherwise route to feature.
