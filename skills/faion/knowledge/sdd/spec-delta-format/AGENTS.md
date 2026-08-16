# Spec Delta Format

## Summary

**One-sentence:** Defines the one-file spec delta — a baseline named by reference and git ref, four operation verbs applied in exactly one order, and a scenario-loss check on every removal and change — so that "what did this feature do to the source of truth?" is answerable from a single reviewable file.

**One-paragraph:** Once `project-spec/` exists, a feature's `spec.md` stops being a full specification and becomes a diff against it. That diff is the highest-leverage document in the repo and the most commonly written by feel: verbs invented per feature, RENAMED expressed as a REMOVED plus an ADDED that quietly loses every reference, and the delta filed away before anyone checked that the merge actually produced a coherent `project-spec/`. This methodology fixes four things. The baseline is named by *reference* plus a git ref, never copied — a copied baseline forks the source of truth the moment the original moves. There are exactly four verbs, RENAMED among them, applied in the order `RENAMED → REMOVED → CHANGED → ADDED`, which is the only order in which each operation sees a consistent world. Every REMOVED and every CHANGED block enumerates the scenarios that referenced it, because the way coverage disappears is not a deleted test but a deleted section that three acceptance criteria were quietly hanging off. And the delta is archived only *after* the merged `project-spec/` verifies, never before — archive-then-verify throws away the instruction set at the exact moment you need it to diagnose what went wrong.

**Ефективно для:**

- Any repo where `project-spec/` is the source of truth and features are expected to update it in the same pull request.
- Reviewers who need to answer "what changed about the system, as opposed to what code was written" without reading the diff.
- Renames — the operation that silently destroys traceability when expressed as a delete plus an add.
- Post-mortems on a `project-spec/` that no longer matches the system, where the deltas are the only reconstructable history.

## Applies If (ALL must hold)

- `project-spec/` (or an equivalent single source of truth for the durable shape of the system) exists and is maintained.
- The feature changes that source of truth — not just the code that implements it.
- The change will be reviewed by someone who did not write it, human or agent.

## Skip If (ANY kills it)

- There is no `project-spec/` yet. Write the full `spec.md` and adopt `sdd/project-spec-structure` first; a delta against nothing is just a spec with confusing headings.
- The change is purely implementation — refactor, dependency bump, performance work — with no effect on the durable shape of the system. Nothing to delta.
- The feature is the one that *creates* `project-spec/`. That is an initial write, not a delta.
- The project keeps a per-feature full spec on purpose (regulated handover, external audit). A delta is not a substitute for a document someone is contractually owed.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Seven testable rules: baseline by reference, the four verbs, the merge order and why it is the only one, the scenario-loss check, bounded Out of Scope, ids inside operation blocks, verify-then-archive. |
| `content/02-output-contract.xml` | The exact file shape, the closed section vocabulary, forbidden patterns, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six ways a delta destroys the thing it was meant to protect. |
| `content/06-decision-tree.xml` | Routing one change to a verb — including the two cases where the answer is "this is not a delta". |
| `scripts/validate-spec-delta-format.py` | Validates a delta file: baseline ref, section vocabulary and order, ids, rename arrows, cross-section id collisions, scenario lines. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-delta.md.j2` | Fill-in delta, ships valid against its own contract. |
| `templates/spec-delta.md` | Fill-in delta, ships valid against its own contract. Generated from `templates/spec-delta.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Related

- `project-spec-structure` — the baseline this file is a delta against. `content/03-delta-update.xml` there mandates a same-PR delta and never defines one; this methodology is that definition. Neither is usable without the other, which is why both sit at the same tier.
- `readiness-checklist` — item `i8-spec-delta` is the gate that asks whether the delta was written and merged. Verify-then-archive is the ordering that item depends on.
- `spec-requirements` — the requirement ids that appear inside `CHANGED` and `ADDED` blocks, and that a `RENAMED` must carry across.
- `architecture-decision-records` — where the *reasoning* behind a change goes. The delta records what changed, not why it was chosen.
